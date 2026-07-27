import 'package:flutter_tts/flutter_tts.dart';

/// Provides step-by-step first aid instructions with text-to-speech narration.
class FirstAidService {
  final FlutterTts _tts = FlutterTts();
  bool _isInitialized = false;

  /// Initialize TTS engine.
  Future<void> initialize() async {
    if (_isInitialized) return;
    await _tts.setLanguage('en-US');
    await _tts.setSpeechRate(0.45); // Slow and clear for emergencies
    await _tts.setVolume(1.0);
    await _tts.setPitch(1.0);
    _isInitialized = true;
  }

  /// Speak the given text aloud.
  Future<void> speak(String text) async {
    await initialize();
    await _tts.speak(text);
  }

  /// Stop speaking.
  Future<void> stop() async {
    await _tts.stop();
  }

  /// Get first aid steps for a given emergency type.
  List<FirstAidStep> getStepsForEmergency(String emergencyType) {
    switch (emergencyType.toLowerCase()) {
      case 'cardiac arrest':
        return _cardiacArrestSteps;
      case 'choking':
        return _chokingSteps;
      case 'severe bleeding':
        return _severeBleedingSteps;
      case 'accident':
        return _accidentSteps;
      case 'drowning':
        return _drowningSteps;
      case 'seizure':
        return _seizureSteps;
      case 'allergic reaction':
        return _allergicReactionSteps;
      default:
        return _generalFirstAidSteps;
    }
  }

  // ── CPR / Cardiac Arrest ──
  static final List<FirstAidStep> _cardiacArrestSteps = [
    FirstAidStep(
      stepNumber: 1,
      title: 'Check Responsiveness',
      description: 'Tap the person\'s shoulders and shout "Are you okay?"',
      substeps: [
        'Tap firmly on both shoulders',
        'Shout loudly near the person\'s ear',
        'Look for breathing or movement',
      ],
    ),
    FirstAidStep(
      stepNumber: 2,
      title: 'Perform Chest Compressions',
      description: 'Push hard and fast in the center of the chest.',
      substeps: [
        'Place heel of hand on center of chest',
        'Interlock fingers',
        'Push down 2 inches at 100-120 bpm',
      ],
    ),
    FirstAidStep(
      stepNumber: 3,
      title: 'Open Airway',
      description: 'Tilt the head back and lift the chin.',
      substeps: [
        'Place one hand on the forehead',
        'Gently tilt the head back',
        'Lift the chin with two fingers',
      ],
    ),
    FirstAidStep(
      stepNumber: 4,
      title: 'Give Rescue Breaths',
      description: 'Pinch the nose and give 2 breaths.',
      substeps: [
        'Pinch the nose shut',
        'Create a complete seal over the mouth',
        'Give 2 breaths each lasting about 1 second',
      ],
    ),
    FirstAidStep(
      stepNumber: 5,
      title: 'Continue CPR',
      description: 'Repeat 30 compressions and 2 breaths.',
      substeps: [
        'Continue cycles of 30:2',
        'Do not stop until help arrives',
        'Switch with another rescuer every 2 minutes if possible',
      ],
    ),
  ];

  // ── Choking ──
  static final List<FirstAidStep> _chokingSteps = [
    FirstAidStep(
      stepNumber: 1,
      title: 'Assess the Situation',
      description: 'Ask "Are you choking?" Look for universal choking sign.',
      substeps: [
        'Check if the person can cough or speak',
        'Look for hands clutching the throat',
        'If they can cough forcefully, encourage them to keep coughing',
      ],
    ),
    FirstAidStep(
      stepNumber: 2,
      title: 'Perform Back Blows',
      description: 'Give 5 firm back blows between the shoulder blades.',
      substeps: [
        'Stand behind or to the side',
        'Support their chest with one hand',
        'Give 5 sharp blows between shoulder blades with heel of hand',
      ],
    ),
    FirstAidStep(
      stepNumber: 3,
      title: 'Perform Abdominal Thrusts',
      description: 'Perform the Heimlich maneuver.',
      substeps: [
        'Stand behind the person, wrap arms around waist',
        'Make a fist and place it above the navel',
        'Grasp the fist and thrust inward and upward',
      ],
    ),
    FirstAidStep(
      stepNumber: 4,
      title: 'Repeat Until Clear',
      description: 'Alternate between back blows and abdominal thrusts.',
      substeps: [
        'Continue alternating 5 back blows and 5 thrusts',
        'If the person becomes unconscious, begin CPR',
        'Look in the mouth before giving breaths',
      ],
    ),
  ];

  // ── Severe Bleeding ──
  static final List<FirstAidStep> _severeBleedingSteps = [
    FirstAidStep(
      stepNumber: 1,
      title: 'Apply Direct Pressure',
      description: 'Press firmly on the wound with a clean cloth.',
      substeps: [
        'Use a clean cloth, towel, or bandage',
        'Apply firm, steady pressure',
        'Do not remove the cloth if blood soaks through — add more',
      ],
    ),
    FirstAidStep(
      stepNumber: 2,
      title: 'Elevate the Wound',
      description: 'Raise the injured area above heart level if possible.',
      substeps: [
        'Keep pressure applied while elevating',
        'If a limb is injured, raise it',
        'Do not elevate if fracture is suspected',
      ],
    ),
    FirstAidStep(
      stepNumber: 3,
      title: 'Apply Bandage',
      description: 'Wrap the wound firmly but not too tight.',
      substeps: [
        'Secure the dressing with a bandage',
        'Ensure circulation beyond the bandage',
        'Check fingers/toes for numbness or color change',
      ],
    ),
  ];

  // ── Accident ──
  static final List<FirstAidStep> _accidentSteps = [
    FirstAidStep(
      stepNumber: 1,
      title: 'Ensure Scene Safety',
      description: 'Make sure the area is safe before approaching.',
      substeps: [
        'Check for oncoming traffic or hazards',
        'Turn off ignition if vehicle accident',
        'Use hazard lights or flares if available',
      ],
    ),
    FirstAidStep(
      stepNumber: 2,
      title: 'Check the Victim',
      description: 'Assess consciousness and breathing.',
      substeps: [
        'Do NOT move the victim unless in danger',
        'Check for responsiveness',
        'Check for breathing and pulse',
      ],
    ),
    FirstAidStep(
      stepNumber: 3,
      title: 'Control Bleeding',
      description: 'Apply pressure to any visible wounds.',
      substeps: [
        'Apply direct pressure with clean cloth',
        'Elevate injured limbs if no fracture suspected',
        'Keep the person warm and calm',
      ],
    ),
  ];

  // ── Drowning ──
  static final List<FirstAidStep> _drowningSteps = [
    FirstAidStep(
      stepNumber: 1,
      title: 'Remove from Water',
      description: 'Get the person out of the water safely.',
      substeps: [
        'Ensure your own safety first',
        'Use a flotation device or reach with an object',
        'Support the head and neck while removing',
      ],
    ),
    FirstAidStep(
      stepNumber: 2,
      title: 'Check Breathing',
      description: 'Assess if the person is breathing.',
      substeps: [
        'Place on firm, flat surface',
        'Tilt head back and lift chin',
        'Look, listen, and feel for breathing',
      ],
    ),
    FirstAidStep(
      stepNumber: 3,
      title: 'Begin CPR if Needed',
      description: 'Start with rescue breaths then compressions.',
      substeps: [
        'Give 2 rescue breaths first',
        'Begin 30 chest compressions',
        'Continue 30:2 cycles until help arrives',
      ],
    ),
  ];

  // ── Seizure ──
  static final List<FirstAidStep> _seizureSteps = [
    FirstAidStep(
      stepNumber: 1,
      title: 'Keep Them Safe',
      description: 'Clear the area around the person.',
      substeps: [
        'Move sharp or hard objects away',
        'Place something soft under their head',
        'Do NOT hold them down or put anything in their mouth',
      ],
    ),
    FirstAidStep(
      stepNumber: 2,
      title: 'Time the Seizure',
      description: 'Note how long the seizure lasts.',
      substeps: [
        'If over 5 minutes, call emergency services immediately',
        'Stay calm and stay with the person',
        'Speak reassuringly',
      ],
    ),
    FirstAidStep(
      stepNumber: 3,
      title: 'Recovery Position',
      description: 'Once seizure stops, turn them on their side.',
      substeps: [
        'Turn into recovery position',
        'Check breathing',
        'Stay with them until fully alert',
      ],
    ),
  ];

  // ── Allergic Reaction ──
  static final List<FirstAidStep> _allergicReactionSteps = [
    FirstAidStep(
      stepNumber: 1,
      title: 'Identify Symptoms',
      description: 'Look for signs of severe allergic reaction.',
      substeps: [
        'Swelling of face, lips, or throat',
        'Difficulty breathing or wheezing',
        'Hives, rash, or skin flushing',
      ],
    ),
    FirstAidStep(
      stepNumber: 2,
      title: 'Use EpiPen if Available',
      description: 'Help administer epinephrine auto-injector.',
      substeps: [
        'Remove safety cap',
        'Inject into outer thigh (through clothing is okay)',
        'Hold for 10 seconds',
      ],
    ),
    FirstAidStep(
      stepNumber: 3,
      title: 'Position and Monitor',
      description: 'Keep them comfortable and monitor breathing.',
      substeps: [
        'If breathing is difficult, have them sit upright',
        'If feeling faint, lay them down with legs elevated',
        'Monitor breathing until help arrives',
      ],
    ),
  ];

  // ── General / Other ──
  static final List<FirstAidStep> _generalFirstAidSteps = [
    FirstAidStep(
      stepNumber: 1,
      title: 'Assess the Situation',
      description: 'Check the scene for safety and assess the victim.',
      substeps: [
        'Ensure the scene is safe for you',
        'Check for responsiveness',
        'Call for additional help',
      ],
    ),
    FirstAidStep(
      stepNumber: 2,
      title: 'Check Vitals',
      description: 'Assess breathing and circulation.',
      substeps: [
        'Check for normal breathing',
        'Check for pulse',
        'Begin CPR if needed',
      ],
    ),
    FirstAidStep(
      stepNumber: 3,
      title: 'Provide Comfort',
      description: 'Keep the person calm and comfortable.',
      substeps: [
        'Keep the person warm',
        'Talk to them reassuringly',
        'Do not give food or drink',
      ],
    ),
  ];
}

/// Represents a single step in a first aid procedure.
class FirstAidStep {
  final int stepNumber;
  final String title;
  final String description;
  final List<String> substeps;

  const FirstAidStep({
    required this.stepNumber,
    required this.title,
    required this.description,
    this.substeps = const [],
  });
}
