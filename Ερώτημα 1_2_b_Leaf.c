#include "contiki.h"
#include "net/netstack.h"
#include "net/nullnet/nullnet.h"
#include "arch/dev/sensor/sht11/sht11-sensor.h"

#include "sys/log.h"
#include "utils.h" 

#include <string.h>
#include <stdio.h>

#define LOG_MODULE "LeafNode"
#define LOG_LEVEL LOG_LEVEL_INFO

#define SEND_INTERVAL (20 * CLOCK_SECOND)

// MAC address of Telos
static linkaddr_t dest_addr = {{ 0xa9, 0xb0, 0x60, 0x13, 0x00, 0x74, 0x12, 0x00 }}; // Hardcoded MAC address of Central Node

PROCESS(leaf_process, "Leaf Node");
AUTOSTART_PROCESSES(&leaf_process);

PROCESS_THREAD(leaf_process, ev, data)
{
  static struct etimer periodic_timer;
  static struct data_form packet;
  static unsigned count = 0;

  PROCESS_BEGIN();

#if MAC_CONF_WITH_TSCH
  static linkaddr_t coordinator_addr = {{ 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }};
  tsch_set_coordinator(linkaddr_cmp(&coordinator_addr, &linkaddr_node_addr));
#endif

  SENSORS_ACTIVATE(sht11_sensor);

  while(1) {
    etimer_set(&periodic_timer, SEND_INTERVAL);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));
int raw_temp = sht11_sensor.value(SHT11_SENSOR_TEMP);
    int raw_hum = sht11_sensor.value(SHT11_SENSOR_HUMIDITY);

    packet.ID = linkaddr_node_addr.u8[0]; // π.χ. θέτει ID στον ασιθητήρα φύλλο -> τελευταίο byte της address
    packet.temp = temperature_int2double(raw_temp);
    packet.hum = humidity_int2double(raw_hum);

    nullnet_buf = (uint8_t *)&packet;
    nullnet_len = sizeof(packet);
    nullnet_set_input_callback(NULL); // Τα φύλλα δεν λαμβάνουν σήμα

    LOG_INFO("ID: %u | #%u | Temp: %.2lf°C | Hum: %.2lf%%\n",
              packet.ID, packet.count, packet.temp, packet.hum);

    NETSTACK_NETWORK.output(&dest_addr);
    count++;
  }

  SENSORS_DEACTIVATE(sht11_sensor);

  PROCESS_END();
}
