import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../core/theme/app_colors.dart';
import '../../services/ai_service.dart';
import '../../services/first_aid_service.dart';

/// First aid guidance screen with AI-powered chat assistant.
class FirstAidGuidanceScreen extends StatefulWidget {
  final String emergencyType;
  final String? emergencyId;

  const FirstAidGuidanceScreen({
    super.key,
    required this.emergencyType,
    this.emergencyId,
  });

  @override
  State<FirstAidGuidanceScreen> createState() => _FirstAidGuidanceScreenState();
}

class _FirstAidGuidanceScreenState extends State<FirstAidGuidanceScreen> {
  final AIService _aiService = AIService();
  final TextEditingController _chatController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<_ChatMessage> _messages = [];

  final FirstAidService _firstAidService = FirstAidService();
  bool _isSpeaking = false;
  bool _isLoadingAI = true;
  bool _isSending = false;


  @override
  void initState() {
    super.initState();


    if (widget.emergencyId != null) {
      _loadAIGuidance();
    } else {
      // General browsing mode — show welcoming screen with quick action chips
      _isLoadingAI = false;
      _messages.add(
        _ChatMessage(
          text: 'Hello! I am **MediRoute AI**, your first aid assistant.\n\n'
              'Select one of the emergency situations below for step-by-step guidance, or type your own question:',
          isUser: false,
        ),
      );
    }
  }

  @override
  void dispose() {

    _chatController.dispose();
    _scrollController.dispose();
    _aiService.dispose();
    _firstAidService.stop();
    super.dispose();
  }

  Future<void> _loadAIGuidance() async {
    final guidance = await _aiService.getFirstAidGuidance(widget.emergencyType);
    setState(() {
      _isLoadingAI = false;
      _messages.add(_ChatMessage(text: guidance, isUser: false));
    });
    _speakText(guidance);
  }

  Future<void> _sendMessage() async {
    final text = _chatController.text.trim();
    if (text.isEmpty || _isSending) return;

    setState(() {
      _messages.add(_ChatMessage(text: text, isUser: true));
      _isSending = true;
    });
    _chatController.clear();
    _scrollToBottom();

    final response = await _aiService.chat(text);
    setState(() {
      _messages.add(_ChatMessage(text: response, isUser: false));
      _isSending = false;
    });
    _scrollToBottom();
    _speakText(response);
  }

  Future<void> _speakText(String text) async {
    setState(() => _isSpeaking = true);
    await _firstAidService.speak(text);
  }

  Future<void> _stopSpeaking() async {
    await _firstAidService.stop();
    if (mounted) {
      setState(() => _isSpeaking = false);
    }
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: Text(widget.emergencyType),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/bystander/home'),
        ),

      ),
      body: Column(
        children: [
          // Status bar
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
            color: AppColors.primaryRed.withValues(alpha: 0.08),
            child: Row(
              children: [
                const Icon(
                  Icons.smart_toy,
                  color: AppColors.primaryRed,
                  size: 18,
                ),
                const SizedBox(width: 8),
                const Expanded(
                  child: Text(
                    'AI First Aid Assistant — Ask anything about the emergency',
                    style: TextStyle(
                      color: AppColors.textSecondary,
                      fontSize: 12,
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 2,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.green.withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Text(
                    'LIVE',
                    style: TextStyle(
                      color: Colors.green,
                      fontSize: 10,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Chat messages
          Expanded(
            child: _isLoadingAI
                ? const Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        CircularProgressIndicator(color: AppColors.primaryRed),
                        SizedBox(height: 16),
                        Text(
                          'AI is preparing first aid guidance...',
                          style: TextStyle(color: AppColors.textSecondary),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length + (_isSending ? 1 : 0),
                    itemBuilder: (context, index) {
                      if (index == _messages.length) {
                        return _buildTypingIndicator();
                      }
                      
                      final msg = _messages[index];
                      final isFirstWelcome = index == 0 && widget.emergencyId == null && _messages.length == 1;

                      if (isFirstWelcome) {
                        return Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            _buildMessageBubble(msg),
                            Padding(
                              padding: const EdgeInsets.only(left: 8, right: 8, bottom: 20),
                              child: Wrap(
                                spacing: 8,
                                runSpacing: 8,
                                children: [
                                  'CPR / Cardiac Arrest',
                                  'Choking Rescue',
                                  'Severe Bleeding',
                                  'Seizure First Aid',
                                  'Allergic Reaction',
                                  'Drowning Rescue',
                                ].map((chipText) {
                                  return ActionChip(
                                    label: Text(
                                      chipText,
                                      style: const TextStyle(color: AppColors.textPrimary, fontSize: 12),
                                    ),
                                    backgroundColor: AppColors.cardBackground,
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(20),
                                      side: const BorderSide(color: AppColors.cardBorder),
                                    ),
                                    onPressed: () {
                                      _chatController.text = 'Give me first aid steps for $chipText.';
                                      _sendMessage();
                                    },
                                  );
                                }).toList(),
                              ),
                            ),
                          ],
                        );
                      }
                      
                      return _buildMessageBubble(msg);
                    },
                  ),
          ),

          // Chat input
          Container(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
            decoration: BoxDecoration(
              color: AppColors.backgroundDark,
              border: Border(top: BorderSide(color: AppColors.divider)),
            ),
            child: SafeArea(
              top: false,
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _chatController,
                      style: const TextStyle(
                        color: AppColors.textPrimary,
                        fontSize: 14,
                      ),
                      decoration: InputDecoration(
                        hintText: 'Ask about the emergency...',
                        hintStyle: const TextStyle(
                          color: AppColors.textSubdued,
                          fontSize: 14,
                        ),
                        filled: true,
                        fillColor: AppColors.cardBackground,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                          borderSide: BorderSide.none,
                        ),
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 10,
                        ),
                      ),
                      onSubmitted: (_) => _sendMessage(),
                    ),
                  ),
                  const SizedBox(width: 8),
                  GestureDetector(
                    onTap: _sendMessage,
                    child: Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: AppColors.primaryRed,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(
                        Icons.send,
                        color: Colors.white,
                        size: 20,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(_ChatMessage msg) {
    final isUser = msg.isUser;
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.8,
        ),
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: isUser
              ? AppColors.primaryRed.withValues(alpha: 0.2)
              : AppColors.cardBackground,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(isUser ? 16 : 4),
            bottomRight: Radius.circular(isUser ? 4 : 16),
          ),
          border: Border.all(
            color: isUser
                ? AppColors.primaryRed.withValues(alpha: 0.3)
                : AppColors.cardBorder,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (!isUser)
              Padding(
                padding: const EdgeInsets.only(bottom: 6),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.smart_toy,
                          color: AppColors.primaryRed,
                          size: 14,
                        ),
                        const SizedBox(width: 4),
                        const Text(
                          'MediRoute AI',
                          style: TextStyle(
                            color: AppColors.primaryRed,
                            fontSize: 11,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ],
                    ),
                    GestureDetector(
                      onTap: () {
                        if (_isSpeaking) {
                          _stopSpeaking();
                        } else {
                          _speakText(msg.text);
                        }
                      },
                      child: Container(
                        padding: const EdgeInsets.all(4),
                        decoration: BoxDecoration(
                          color: AppColors.primaryRed.withValues(alpha: 0.1),
                          shape: BoxShape.circle,
                        ),
                        child: Icon(
                          _isSpeaking ? Icons.volume_up : Icons.volume_mute,
                          color: AppColors.primaryRed,
                          size: 14,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            _buildFormattedText(msg.text),
          ],
        ),
      ),
    );
  }

  Widget _buildFormattedText(String text) {
    final spans = <TextSpan>[];
    final lines = text.split('\n');

    for (int i = 0; i < lines.length; i++) {
      String line = lines[i];

      // Detect bullet points (starts with *, -, or a number followed by dot)
      bool isBullet = line.trimLeft().startsWith('* ') || 
                      line.trimLeft().startsWith('- ') || 
                      RegExp(r'^\d+\.\s').hasMatch(line.trimLeft());

      if (isBullet) {
        spans.add(
          const TextSpan(
            text: '\n• ',
            style: TextStyle(color: AppColors.primaryRed, fontWeight: FontWeight.bold),
          ),
        );
        line = line.replaceFirst(RegExp(r'^(\*\s|-\s|\d+\.\s)'), '');
      } else if (i > 0) {
        spans.add(const TextSpan(text: '\n'));
      }

      // Regex for **bold**
      final regExp = RegExp(r'\*\*(.*?)\*\*');
      int lastIndex = 0;

      for (final match in regExp.allMatches(line)) {
        if (match.start > lastIndex) {
          spans.add(
            TextSpan(
              text: line.substring(lastIndex, match.start),
              style: const TextStyle(color: AppColors.textPrimary),
            ),
          );
        }
        spans.add(
          TextSpan(
            text: match.group(1),
            style: const TextStyle(
              color: AppColors.textPrimary,
              fontWeight: FontWeight.bold,
            ),
          ),
        );
        lastIndex = match.end;
      }

      if (lastIndex < line.length) {
        spans.add(
          TextSpan(
            text: line.substring(lastIndex),
            style: const TextStyle(color: AppColors.textPrimary),
          ),
        );
      }
    }

    return RichText(
      text: TextSpan(
        style: const TextStyle(
          fontSize: 14,
          height: 1.5,
          color: AppColors.textPrimary,
        ),
        children: spans,
      ),
    );
  }

  Widget _buildTypingIndicator() {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: AppColors.cardBackground,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            SizedBox(
              width: 16,
              height: 16,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                color: AppColors.primaryRed,
              ),
            ),
            const SizedBox(width: 8),
            const Text(
              'AI is thinking...',
              style: TextStyle(color: AppColors.textSecondary, fontSize: 13),
            ),
          ],
        ),
      ),
    );
  }
}

class _ChatMessage {
  final String text;
  final bool isUser;
  _ChatMessage({required this.text, required this.isUser});
}
