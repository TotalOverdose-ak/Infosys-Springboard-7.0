class Subsidy {
  final String id;
  final String title;
  final String description;
  final double amount;
  final String eligibilityCriteria;
  final String? applicationDeadline;
  final String state;
  final String category;
  final bool isActive;
  final String? applicationUrl;
  final List<String> documentsRequired;

  Subsidy({
    required this.id,
    required this.title,
    required this.description,
    required this.amount,
    required this.eligibilityCriteria,
    this.applicationDeadline,
    required this.state,
    required this.category,
    required this.isActive,
    this.applicationUrl,
    this.documentsRequired = const [],
  });

  factory Subsidy.fromJson(Map<String, dynamic> json) {
    return Subsidy(
      id: json['id'] ?? '',
      title: json['title'] ?? 'No Title',
      description: json['description'] ?? 'No Description',
      amount: (json['amount'] ?? 0).toDouble(),
      eligibilityCriteria: json['eligibilityCriteria'] ?? 'Not specified',
      applicationDeadline: json['applicationDeadline'],
      state: json['state'] ?? 'All States',
      category: json['category'] ?? 'General',
      isActive: json['isActive'] ?? true,
      applicationUrl: json['applicationUrl'],
      documentsRequired: (json['documentsRequired'] as List<dynamic>?)?.map((e) => e.toString()).toList() ?? [],
    );
  }

  // Generate YouTube search URL for help videos about this scheme
  String get youtubeHelpUrl =>
      'https://www.youtube.com/results?search_query=${Uri.encodeComponent("$title scheme how to apply")}';  

  // Check if the scheme deadline has passed
  bool get isExpired {
    if (applicationDeadline == null) return false;
    try {
      final deadline = DateTime.parse(applicationDeadline!);
      return DateTime.now().isAfter(deadline);
    } catch (_) {
      return false;
    }
  }
}
