import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService extends GetxService {
  String baseUrl = 'http://localhost:6002'; // Replace with your Flask API base URL

  static Future<Map<String, dynamic>> getMortgageRange(String location) async {
    final url = Uri.parse('http://localhost:6002/data/mortgage_range?location=$location');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load mortgage range data');
    }
  }

  static Future<List<dynamic>> getPriceTrend(String location, int year) async {
    final url = Uri.parse('http://localhost:6002/data/price_trend?location=$location&year=$year');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load price trend data');
    }
  }

  static Future<Map<String, dynamic>> getAveragePrice(String location) async {
    final url = Uri.parse('http://localhost:6002/data/average_price?location=$location');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load average price data');
    }
  }

  static Future<Map<String, dynamic>> getPricesOverTime(String location, {int? yearMin, int? yearMax}) async {
    // Build the URL with optional year parameters
    String url = 'http://localhost:6002/data/prices_over_time/$location';

    if (yearMin != null && yearMax != null) {
      url += '?year_min=$yearMin&year_max=$yearMax';
    } else if (yearMin != null) {
      url += '?year_min=$yearMin';
    } else if (yearMax != null) {
      url += '?year_max=$yearMax';
    }

    final response = await http.get(Uri.parse(url));

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load price trend data over time');
    }
  }

  // Add more methods to fetch data from other endpoints
}
