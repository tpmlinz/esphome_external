from esphome import automation
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
#    CONF_ON_STATE,
    CONF_TRIGGER_ID,
    CONF_INVERT,
    DEVICE_CLASS_TEMPERATURE,
    CONF_TARGET_TEMPERATURE,
    CONF_TARGET_TEMPERATURE_LOW,
    CONF_TARGET_TEMPERATURE_HIGH,    
    DEVICE_CLASS_SPEED,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_PERCENT,
#    CONF_SENSOR,
    DEVICE_CLASS_TEMPERATURE,
)

CONF_ERROR = "error"
CONF_PWM_IN = "pwm_in"
CONF_PWM_OUT = "pwm_out"



# Namespace
upm3_sensor_ns = cg.esphome_ns.namespace("upm3_sensor")

# Class
UPM3Sensor = upm3_sensor_ns.class_("UPM3Sensor",  cg.PollingComponent)

#PWMData = upm3_sensor_ns.class_("PWMData",  cg.PollingComponent)


# Actions
UPM3AutomationSetErrorAction = upm3_sensor_ns.class_(
    "UPM3AutomationSetErrorAction", automation.Action
)

# Conditions
UPM3AutomationCondition = upm3_sensor_ns.class_(
    "UPM3AutomationCondition",  automation.Condition
)

# Triggers
UPM3StateTrigger = upm3_sensor_ns.class_(
    "UPM3StateTrigger",  automation.Trigger.template(bool)
)

UPM3_AUTOMATION_ACTION_SCHEMA = cv.maybe_simple_value(
    {
        cv.Required(CONF_ID): cv.use_id(UPM3Sensor),
        cv.Required(CONF_ERROR): cv.boolean,
    },
    key=CONF_ERROR,
)

UPM3_AUTOMATION_CONDITION_SCHEMA = automation.maybe_simple_id(
    {
        cv.Required(CONF_ID): cv.use_id(UPM3Sensor),
    }
)


UPM3_PWM_SCHEMA = cv.Schema(
  {
    #cv.GenerateID(): cv.declare_id(PWMData),
    cv.Optional(CONF_INVERT): cv.boolean,    
  }
)



CONFIG_SCHEMA = cv.Schema(
  {
        cv.GenerateID(): cv.declare_id(UPM3Sensor),
        
        cv.Optional(CONF_ON_ERROR): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(UPM3StateTrigger),
            }
        ),
        
        ###########
        cv.Optional(CONF_PWM_IN):  UPM3_PWM_SCHEMA,
        cv.Optional(CONF_PWM_OUT):  UPM3_PWM_SCHEMA,
		#######
        
        #################
 		cv.Optional(CONF_TARGET_TEMPERATURE): cv.int_range(0, 100),
        cv.Optional(CONF_TARGET_TEMPERATURE_LOW): cv.int_range(0, 100),
        cv.Optional(CONF_TARGET_TEMPERATURE_HIGH): cv.int_range(0, 100),
        ###################        
        #cv.Optional(CONF_TARGET_TEMPERATURE): cv.int_range(35, 65),          
        #cv.Optional(CONF_TARGET_TEMPERATURE_HIGH): cv.int_range(40, 70),  
        #cv.Optional(CONF_TARGET_TEMPERATURE_LOW): cv.int_range(5, 30),
        ###################
        #cv.Optional(CONF_INVERT): cv.bool_        
        #
                 
        cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        
        cv.Optional(CONF_SPEED): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_SPEED,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
		      
  }
).extend(cv.polling_component_schema("60s"))



#####################
# register_action
@automation.register_action(
    "upm3_sensor.set_error",
    UPM3AutomationSetErrorAction,
    UPM3_AUTOMATION_ACTION_SCHEMA,
)


async def upm3_automation_set_error_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    cg.add(var.set_error(config[CONF_ERROR]))
    return var



async def upm3_automation_condition_to_code(
    config, condition_id, template_arg, args
):
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(condition_id, template_arg, paren, True)



####################
# register_condition
@automation.register_condition(
    "upm3_sensor.has_error",
    UPM3AutomationCondition,
    UPM3_AUTOMATION_CONDITION_SCHEMA,
)

#########################
# upm3_automation_on_to_code
async def upm3_automation_on_condition_to_code(
    config, condition_id, template_arg, args
):
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(condition_id, template_arg, paren, True)


########################
# to_code
async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    
    if pwmInConf := config.get(CONF_PWM_IN):
      if inv := pwmInConf.get(CONF_INVERT):
        cg.add(var.set_invert_PWM(0, True)) 
    
    if CONF_TEMPERATURE in config:
       sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
       cg.add(var.setTemperatureSensor(sens))
       
    if CONF_SPEED in config:
       sens = await sensor.new_sensor(config[CONF_SPEED])
       cg.add(var.setSpeedSensor(sens))

    if targetTemperature := config.get(CONF_TARGET_TEMPERATURE):
       cg.add(var.setTargetTemperature(targetTemperature))
	    
    if targetTemperatureHigh := config.get(CONF_TARGET_TEMPERATURE_HIGH):
       cg.add(var.setTargetTemperatureHigh(targetTemperature))
	    
    if targetTemperatureLow := config.get(CONF_TARGET_TEMPERATURE_LOW):
       cg.add(var.setTargetTemperatureLow(targetTemperature))
       
    for conf in config.get(CONF_ON_ERROR, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [(bool, "x")], conf)
     