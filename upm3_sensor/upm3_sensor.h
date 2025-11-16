#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"

namespace esphome {
namespace upm3_sensor {

class UPM3Sensor : public PollingComponent {
public:
  void setup() override;
  float get_setup_priority() const override;  
  void update() override;
  void dump_config() override;
  
  void setTemperatureSensor(sensor::Sensor *sens) { m_temperatureSensor = sens; }
  void setSpeedSensor(sensor::Sensor *sens) { m_speedSensor = sens; }
  
   void addErrorCallback(std::function<void()> &&callback);
  void setError(bool state) ;
private:
    sensor::Sensor* m_temperatureSensor{ nullptr };
    sensor::Sensor* m_speedSensor{ nullptr };  
    CallbackManager<void()> m_errorCallback{};
};

class UPM3SensorOnErrorTrigger : public Trigger<> {
public:
  explicit UPM3SensorOnErrorTrigger(UPM3Sensor* parent) {
    parent->addErrorCallback( [this]() { this->trigger(); } );
  }
};

} //namespace upm3_sensor
} //namespace esphome
