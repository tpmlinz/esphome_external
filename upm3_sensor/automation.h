#pragma once

#include "esphome/core/component.h"
#include "esphome/core/automation.h"
#include "upm3_sensor.h"

namespace esphome {
namespace upm3_sensor {

	template<typename ... Ts>
	class UPM3AutomationSetErrorAction: public Action<Ts...> {
	public:
		explicit UPM3AutomationSetErrorAction(UPM3Sensor *upm3) : m_UPM3(upm3) {}
		
		TEMPLATABLE_VALUE(bool, error)
	
		void play(Ts... x) override {
			auto val = error_.value(x...);
			m_UPM3->set_error(val);
		}
	
	protected:
		UPM3Sensor *m_UPM3;
	};
	
	
	
	template<typename ... Ts> 
	class UPM3AutomationCondition: public Condition<Ts...> {
	public:
		
		UPM3AutomationCondition(UPM3Sensor *parent, bool errorFlag) : m_parent(parent), m_errorFlag(errorFlag) {}
		
		bool check(Ts ... x) override { return m_parent->m_errorFlag == m_errorFlag; }
	
	protected:
		UPM3Sensor *m_parent;
		bool m_errorFlag;
	};
	
	
	
	class UPM3StateTrigger: public Trigger<bool> {
	public:
		explicit UPM3StateTrigger(UPM3Sensor *parent) {
			parent->addOnErrorCallback( [this](bool errorFlag){ this->trigger(errorFlag);} );
		}
	};

}  // upm3_sensor empty_automation
}  // namespace esphome
