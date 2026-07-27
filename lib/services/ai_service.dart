import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:flutter/foundation.dart';

/// AI-powered emergency assistant using Gemini.
class AIService {
  static const _apiKey = String.fromEnvironment(
    'GEMINI_API_KEY',
    defaultValue: '',
  );
  late final GenerativeModel _model;
  ChatSession? _chatSession;

  AIService() {
    _model = GenerativeModel(
      model: 'gemini-2.5-flash',
      apiKey: _apiKey,
      systemInstruction: Content.system(
        'You are MediRoute AI — an emergency medical assistant. '
        'You provide clear, step-by-step first aid instructions. '
        'Always be calm, direct, and concise. '
        'Prioritize life-saving actions. '
        'If the situation is beyond first aid, clearly advise calling emergency services. '
        'Keep responses under 150 words. Use numbered steps when giving instructions.',
      ),
    );
  }

  /// Start a new chat session for an emergency type.
  void startSession(String emergencyType) {
    _chatSession = _model.startChat(
      history: [
        Content.text(
          'I am a bystander at a medical emergency. '
          'The emergency type is: $emergencyType. '
          'Please guide me through first aid steps.',
        ),
      ],
    );
  }

  /// Send a message and get AI response.
  Future<String> chat(String message) async {
    try {
      _chatSession ??= _model.startChat();
      final response = await _chatSession!.sendMessage(Content.text(message));
      return response.text ??
          'I could not generate a response. Please try again.';
    } catch (e) {
      debugPrint('AI Service error: $e');
      return 'Unable to connect to AI assistant. Please follow the on-screen instructions.';
    }
  }

  /// Get initial first aid guidance for an emergency type.
  Future<String> getFirstAidGuidance(String emergencyType) async {
    try {
      startSession(emergencyType);
      final response = await _chatSession!.sendMessage(
        Content.text(
          'Give me the most critical first aid steps for $emergencyType right now. '
          'Be concise and actionable.',
        ),
      );
      return response.text ?? 'Follow standard first aid procedures.';
    } catch (e) {
      debugPrint('AI guidance error: $e');
      return 'AI is unavailable. Follow the on-screen first aid steps.';
    }
  }

  /// Dispose the chat session.
  void dispose() {
    _chatSession = null;
  }
}
