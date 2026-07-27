// ignore_for_file: avoid_web_libraries_in_flutter
import 'dart:async';
import 'dart:js_interop';
import 'package:flutter/material.dart';
import 'package:web/web.dart' as web;
import '../data/models/hospital_model.dart';

/// Fetches nearby hospitals on Web using the Google Maps JavaScript Places library.
/// This avoids CORS issues that block the REST API from the browser.
class PlacesWebService {
  /// Search for nearby hospitals using the Google Maps JS Places API.
  Future<List<HospitalModel>> fetchNearbyHospitals({
    required double latitude,
    required double longitude,
    double radiusMeters = 5000,
  }) async {
    try {
      // Create a hidden div for PlacesService (it requires an HTML element or map)
      final div = web.document.createElement('div') as web.HTMLDivElement;

      final service = _PlacesServiceJS(div);
      final location = _LatLngJS(latitude.toJS, longitude.toJS);

      final request = _createNearbySearchRequest(
        location: location,
        radius: radiusMeters,
        type: 'hospital',
      );

      final completer = Completer<List<HospitalModel>>();

      void handleResults(JSArray? results, JSAny status) {
        final statusStr = (status as JSString).toDart;
        if (statusStr == 'OK' && results != null) {
          final hospitals = <HospitalModel>[];
          final dartResults = results.toDart;
          for (int i = 0; i < dartResults.length; i++) {
            final place = dartResults[i] as _PlaceResultJS?;
            if (place == null) continue;

            final geometry = place.geometry;
            if (geometry == null) continue;

            final loc = geometry.location;
            if (loc == null) continue;

            final lat = loc.lat().toDartDouble;
            final lng = loc.lng().toDartDouble;
            final name = place.name?.toDart ?? 'Hospital';
            final placeId = place.place_id?.toDart ?? 'place_$i';
            final vicinity = place.vicinity?.toDart ?? '';

            hospitals.add(
              HospitalModel(
                hospitalId: placeId,
                name: name,
                latitude: lat,
                longitude: lng,
                phone: '',
                address: vicinity,
                active: true,
              ),
            );
          }
          completer.complete(hospitals);
        } else {
          debugPrint('Places JS status: $statusStr');
          completer.complete([]);
        }
      }

      service.nearbySearch(request, handleResults.toJS);

      return await completer.future.timeout(
        const Duration(seconds: 10),
        onTimeout: () => [],
      );
    } catch (e) {
      debugPrint('PlacesWebService error: $e');
      return [];
    }
  }
}

// ─── Helper to create the request object as a JS literal ────────────

JSObject _createNearbySearchRequest({
  required _LatLngJS location,
  required double radius,
  required String type,
}) {
  return _jsCreateObject(location, radius.toJS, type.toJS);
}

// Use Reflect.set to create a plain JS object with the correct shape
JSObject _jsCreateObject(_LatLngJS location, JSNumber radius, JSString type) {
  // Build a plain JS object
  final obj = _newObject();
  _setObjectProperty(obj, 'location', location);
  _setObjectProperty(obj, 'radius', radius);
  _setObjectProperty(obj, 'type', type);
  return obj;
}

@JS('Object.create')
external JSObject _createEmptyObject(JSAny? proto);

JSObject _newObject() => _createEmptyObject(null);

// Use bracket-based property assignment via a helper
@JS('Reflect.set')
external JSBoolean _reflectSet(JSObject target, JSString key, JSAny value);

void _setObjectProperty(JSObject obj, String key, JSAny value) {
  _reflectSet(obj, key.toJS, value);
}

// ─── JS Interop bindings for Google Maps Places ─────────────────────

@JS('google.maps.LatLng')
extension type _LatLngJS._(JSObject _) implements JSObject {
  external factory _LatLngJS(JSNumber lat, JSNumber lng);
  external JSNumber lat();
  external JSNumber lng();
}

@JS('google.maps.places.PlacesService')
extension type _PlacesServiceJS._(JSObject _) implements JSObject {
  external factory _PlacesServiceJS(web.HTMLDivElement div);
  external void nearbySearch(JSObject request, JSFunction callback);
}

extension type _PlaceResultJS._(JSObject _) implements JSObject {
  external _PlaceGeometryJS? get geometry;
  external JSString? get name;
  // ignore: non_constant_identifier_names
  external JSString? get place_id;
  external JSString? get vicinity;
}

extension type _PlaceGeometryJS._(JSObject _) implements JSObject {
  external _LatLngJS? get location;
}
