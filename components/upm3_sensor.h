#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"


// macro for logging
// TRUEFALSE(expr) -> "true" ? "false"


/*
 * RENAME ALL PUBLIC METHODS WITH UNDERSCORE INSTEAD OF CAMEL-CASE
 */

namespace esphome {
namespace upm3_sensor {


	class UPM3Sensor: public PollingComponent {
	public:

	// overrides
	void setup() override;
	float get_setup_priority() const override;
	void update() override;
	void dump_config() override;

	// set sensors
	void setTemperatureSensor(sensor::Sensor *sens) { m_temperatureSensor = sens; }
	void setSpeedSensor(sensor::Sensor *sens) { m_speedSensor = sens; }

	// set temperatures
	void setTargetTemperature(int);
	void setTargetTemperatureLow(int);
	void setTargetTemperatureHigh(int);

	// state
	void addOnErrorCallback(std::function<void(bool)> &&callback);
	bool get_error() const { return m_errorFlag; }
	int get_status() const { return m_status; }

	bool m_errorFlag = false;;

	//PWM
	void set_invert_PWM(unsigned idx, bool flag){ if(idx < 2) m_PWM[idx].invert = flag; }

	//wibble

private:
	uint16_t m_targetTemperature;
	uint16_t m_targetTemperatureLow;
	uint16_t m_targetTemperatureHigh;

	sensor::Sensor *m_temperatureSensor { nullptr };
	sensor::Sensor *m_speedSensor { nullptr };

	CallbackManager<void(bool)> m_errorCallback { };

	void set_error(bool);
	int m_status = 42;


	struct PWMConfig{
		bool invert = false;
	};
	PWMConfig m_PWM[2];
};


} //namespace upm3_sensor
} //namespace esphome
