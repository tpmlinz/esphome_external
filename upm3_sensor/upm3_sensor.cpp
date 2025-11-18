#include "upm3_sensor.h"
#include "esphome/core/helpers.h"
#include "esphome/core/log.h"

#include "/home/terry/MX500/Documents/ESP32/workspace/UMP3-ESP32-C-DEVKIT-1/components/UPM3/include/UPM3.h"


namespace{
   const char *TAG  = "UPM3";
} //ns anon



namespace esphome {
namespace upm3_sensor {


	void UPM3Sensor::setup() {
	  //upm3::UPM3::setup();
	  PollingComponent::setup();
	  disable_loop();
	}

	float UPM3Sensor::get_setup_priority() const { return setup_priority::DATA; }

	void UPM3Sensor::update() {

		const auto& upm = upm3::UPM3::getInstance();
		const auto temperature = static_cast<float>(upm.getTemperature());
		const auto speed = static_cast<float>(upm.getInputDutyCycle()) / 10.0f;

		  m_temperatureSensor->publish_state(temperature);
		  m_speedSensor->publish_state(speed);


	}

	void UPM3Sensor::dump_config() {
		ESP_LOGCONFIG(TAG, "UPM3 sensor");
		//LOG_PIN("  Pin: ", this->pin_);
	  //ESP_LOGCONFIG(TAG, "  Internal pull-up: %s", ONOFF(this->pin_->get_flags() & gpio::FLAG_PULLUP));
	  LOG_UPDATE_INTERVAL(this);
	  LOG_SENSOR("  ", "Temperature",  m_temperatureSensor);
	  LOG_SENSOR("  ", "Speed",  m_speedSensor);
	}


	void UPM3Sensor::setTargetTemperature(int t){
		 m_targetTemperature = static_cast<uint16_t>(t);
	}

	void UPM3Sensor::setTargetTemperatureLow(int t){
		m_targetTemperatureLow = static_cast<uint16_t>(t);

	}
	void UPM3Sensor::setTargetTemperatureHigh(int t){
		m_targetTemperatureHigh = static_cast<uint16_t>(t);

	}


	void UPM3Sensor::addOnErrorCallback(std::function<void(bool)> &&callback){
		 m_errorCallback.add(std::move(callback));
	}

	void UPM3Sensor::set_error(bool errorFlag) {
	  ESP_LOGD(TAG, "Set error to %s", TRUEFALSE(errorFlag));
	  m_errorFlag = errorFlag;
	  m_errorCallback.call(errorFlag);
	}


} //namespace upm3_sensor
} //namespace esphome
