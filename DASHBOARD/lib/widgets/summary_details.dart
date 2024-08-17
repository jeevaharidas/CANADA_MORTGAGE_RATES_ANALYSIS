import 'package:fitness_dashboard_ui/controllers/mortgage_controller.dart';
import 'package:fitness_dashboard_ui/widgets/custom_card_widget.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:loading_animation_widget/loading_animation_widget.dart';

class SummaryDetails extends StatefulWidget {
  const SummaryDetails({super.key});

  @override
  State<SummaryDetails> createState() => _SummaryDetailsState();
}

class _SummaryDetailsState extends State<SummaryDetails> {
  MortgageController mortgageController = Get.find();
  @override
  Widget build(BuildContext context) {
    return Obx(() {
      return mortgageController.isLoading.value
          ? LoadingAnimationWidget.prograssiveDots(
              color: const Color(0xFFEA3799),
              size: 200,
            )
          : CustomCard(
              color: const Color(0xFF2F353E),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  buildDetails('Average', mortgageController.averagePrice.toInt().toString()),
                  buildDetails('Trending (2023)', "\$" + mortgageController.priceTrend[0]["average_price"].toInt().toString()),
                  buildDetails('Lowest', "\$" + mortgageController.lowestMortgage.toInt().toString()),
                  buildDetails('Highest', "\$" + mortgageController.highestMortgage.toInt().toString()),
                ],
              ),
            );
    });
  }

  Widget buildDetails(String key, String value) {
    return Column(
      children: [
        Text(
          key,
          style: const TextStyle(fontSize: 11, color: Colors.grey),
        ),
        const SizedBox(height: 2),
        Text(
          value,
          style: const TextStyle(fontSize: 14),
        ),
      ],
    );
  }
}
