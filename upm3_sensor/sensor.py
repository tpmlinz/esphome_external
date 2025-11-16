#from esphome import automation
import esphome.codegen as cg
from esphome.components import sensor
#from esphome.components import number
import esphome.config_validation as cv

from esphome.const import (
    CONF_ID,
    CONF_ON_ERROR,
    CONF_SPEED,
    CONF_TEMPERATURE,
    CONF_STATE,
    CONF_TRIGGER_ID,
    DEVICE_CLASS_TEMPERATURE,
    CONF_TARGET_TEMPERATURE_LOW,
    CONF_TARGET_TEMPERATURE_HIGH,    
    DEVICE_CLASS_SPEED,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_PERCENT,
#    CONF_SENSOR,
    DEVICE_CLASS_TEMPERATURE,
)



#CONF_TARGET_TEMPERATURE_LOW
#CONF_TARGET_TEMPERATURE_HIGH
#DEVICE_CLASS_FREQUENCY
#DEVICE_CLASS_TEMPERATURE
#UNIT_PERCENT
#UNIT_CELSIUS
#DEVICE_CLASS_SPEED
#UNIT_REVOLUTIONS_PER_MINUTE
#CONF_PERIOD
#CONF_VERSION

upm3_sensor_ns = cg.esphome_ns.namespace("upm3_sensor")
UPM3Sensor = upm3_sensor_ns.class_("UPM3Sensor",  cg.PollingComponent)

# Conditions
#UPM3AutomationCondition = upm3_sensor_ns.class_("UPM3AutomationCondition",  automation.Condition)

# Triggers
#UPM3StateTrigger = upm3_sensor_ns.class_("UPM3StateTrigger",  automation.Trigger.template(bool))


CONFIG_SCHEMA = cv.Schema(
  {
        cv.GenerateID(): cv.declare_id(UPM3Sensor),           
        cv.Optional(CONF_TARGET_TEMPERATURE_HIGH): cv.int_range(0, 100),  
        cv.Optional(CONF_TARGET_TEMPERATURE_LOW): cv.int_range(0, 100),         
        cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ) ,
        cv.Optional(CONF_SPEED): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_SPEED,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
  }
).extend(cv.polling_component_schema("60s"))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    
    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.setTemperatureSensor(sens))
    if CONF_SPEED in config:
        sens = await sensor.new_sensor(config[CONF_SPEED])
        cg.add(var.setSpeedSensor(sens))

