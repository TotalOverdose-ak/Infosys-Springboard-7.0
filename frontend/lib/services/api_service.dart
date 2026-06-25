import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/subsidy.dart';

class ApiService {
  // Use 10.0.2.2 instead of localhost if running on Android Emulator
  static const String baseUrl = 'http://127.0.0.1:8080/api';

  // ==================== AUTH ====================

  Future<Map<String, dynamic>> login({required String email, required String password}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'email': email, 'password': password}),
      );
      return json.decode(response.body);
    } catch (e) {
      throw Exception('Connection error: $e');
    }
  }

  Future<Map<String, dynamic>> register({
    required String fullName,
    required String email,
    required String password,
    required String aadharNumber,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/register'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'fullName': fullName,
          'email': email,
          'password': password,
          'aadharNumber': aadharNumber,
        }),
      );
      return json.decode(response.body);
    } catch (e) {
      throw Exception('Connection error: $e');
    }
  }

  // ==================== SUBSIDIES ====================

  Future<List<Subsidy>> fetchSubsidies({String? state, String? category, String? search, int limit = 20}) async {
    try {
      String url = '$baseUrl/subsidies';
      
      final uri = Uri.parse(url);
      final queryParams = <String, String>{};
      
      if (state != null && state.isNotEmpty && state != 'All States') queryParams['state'] = state;
      if (category != null && category.isNotEmpty && category != 'All Categories') queryParams['category'] = category;
      if (search != null && search.isNotEmpty) queryParams['search'] = search;
      queryParams['limit'] = limit.toString();
      
      url = uri.replace(queryParameters: queryParams).toString();

      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        List<dynamic> jsonList = json.decode(response.body);
        return jsonList.map((json) => Subsidy.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load subsidies');
      }
    } catch (e) {
      throw Exception('Error fetching subsidies: $e');
    }
  }

  // Trigger dynamic sync from remote sources
  Future<Map<String, dynamic>> syncSchemes() async {
    try {
      final response = await http.post(Uri.parse('$baseUrl/subsidies/sync'));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Sync failed');
      }
    } catch (e) {
      throw Exception('Error syncing: $e');
    }
  }

  // ==================== APPLICATIONS ====================
  
  Future<Map<String, dynamic>> submitApplication(Map<String, dynamic> data) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/applications'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to submit application: ${response.body}');
      }
    } catch (e) {
      throw Exception('Connection error: $e');
    }
  }
}
