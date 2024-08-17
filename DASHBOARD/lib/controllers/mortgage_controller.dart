import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../services/api_service.dart';

class MortgageController extends GetxController {
  var highestMortgage = 0.0.obs;
  var lowestMortgage = 0.0.obs;
  var location = "Toronto".obs;
  var averagePrice = 0.0.obs;
  var priceTrend = [].obs;
  var priceTrend2 = <Map<String, dynamic>>[].obs;
  var spots = <FlSpot>[].obs;
  var isLoading = false.obs;
  TextEditingController searchController = TextEditingController();
  @override
  void onInit() {
    super.onInit();
    fetchMortgageRange(location.value);
    fetchPriceTrend(location.value, 2023);
    fetchAveragePrice(location.value);
    fetchPriceTrendOverTime(location.value);
  }

  void performSearch() {
    fetchMortgageRange(location.value);
    fetchPriceTrend(location.value, 2023);
    fetchAveragePrice(location.value);
    fetchPriceTrendOverTime(location.value);
  }

  // Generate spots for a line chart from the price trend data
  List<FlSpot> get priceTrendSpots {
    return priceTrend2.map((data) {
      double year = data['year'].toDouble();
      double price = data['average_price'].toDouble();
      return FlSpot(year, price);
    }).toList();
  }

  SideTitles get leftTitles {
    final maxPrice = priceTrend2.map((e) => e['average_price']).reduce((a, b) => a > b ? a : b);
    final minPrice = priceTrend2.map((e) => e['average_price']).reduce((a, b) => a < b ? a : b);

    return SideTitles(
      showTitles: true,
      reservedSize: 40,
      interval: (maxPrice - minPrice) / 5,
      getTitlesWidget: (value, meta) {
        return Text(
          value.round().toString(),
          style: TextStyle(color: Colors.grey[400], fontSize: 12),
        );
      },
    );
  }

  SideTitles get bottomTitles {
    return SideTitles(
      showTitles: true,
      reservedSize: 40,
      interval: 5, // Adjust this interval based on how many years you want to display
      getTitlesWidget: (value, meta) {
        return Text(
          value.toInt().toString(),
          style: TextStyle(color: Colors.grey[400], fontSize: 12),
        );
      },
    );
  }

  Future<void> fetchMortgageRange(String location) async {
    try {
      final data = await ApiService.getMortgageRange(location);
      highestMortgage.value = data['highest_mortgage'];
      lowestMortgage.value = data['lowest_mortgage'];

      print(data);
    } catch (e) {
      Get.snackbar('Error', e.toString());
    }
  }

  Future<void> fetchPriceTrend(String location, int year) async {
    isLoading(true);
    try {
      final data = await ApiService.getPriceTrend(location, year);
      priceTrend.value = data;
      print(data);
      isLoading(false);
    } catch (e) {
      isLoading(false);
      Get.snackbar('Error', e.toString());
    }
  }

  Future<void> fetchAveragePrice(String location) async {
    isLoading(true);

    try {
      final data = await ApiService.getAveragePrice(location);
      averagePrice.value = data['average_price'];
      print(averagePrice.value);
      isLoading(false);
    } catch (e) {
      isLoading(false);

      Get.snackbar('Error', e.toString());
    }
  }

  Future<void> fetchPriceTrendOverTime(String location) async {
    isLoading(true);

    try {
      final data = await ApiService.getPricesOverTime(location);
      var priceTrend = List<Map<String, dynamic>>.from(data['price_trend']);

      // Convert the fetched data into FlSpot objects and save them in the spots list
      spots.value = priceTrend.map((data) {
        double year = data['year'].toDouble();
        double price = data['average_price'].toDouble();
        return FlSpot(year, price);
      }).toList();
      isLoading(false);

      print(spots); // Optional: print the spots for debugging
    } catch (e) {
      isLoading(false);
      Get.snackbar('Error', e.toString());
    }
  }
}
