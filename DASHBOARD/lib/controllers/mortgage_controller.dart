import 'package:get/get.dart';
import '../services/api_service.dart';

class MortgageController extends GetxController {
  var highestMortgage = 0.0.obs;
  var lowestMortgage = 0.0.obs;
  var location = "Toronto".obs;
  var averagePrice = 0.0.obs;
  var priceTrend = [].obs;

  @override
  void onInit() {
    super.onInit();
    fetchMortgageRange(location.value);
    fetchPriceTrend(location.value, 2023);
    fetchAveragePrice(location.value);
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
    try {
      final data = await ApiService.getPriceTrend(location, year);
      priceTrend.value = data;
      print(data);
    } catch (e) {
      Get.snackbar('Error', e.toString());
    }
  }

  Future<void> fetchAveragePrice(String location) async {
    try {
      final data = await ApiService.getAveragePrice(location);
      averagePrice.value = data['average_price'];
      print(averagePrice.value);
    } catch (e) {
      Get.snackbar('Error', e.toString());
    }
  }
}
