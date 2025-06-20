include "contiki.h"
#include "net/netstack.h"
#include "net/nullnet/nullnet.h"
#include "sys/log.h"
#include "utils.h"  
#include <string.h>
#include <stdio.h>

#define LOG_MODULE "TelosB-Central"
#define LOG_LEVEL LOG_LEVEL_INFO

PROCESS(receiver_process, "TelosB");
AUTOSTART_PROCESSES(&receiver_process);

/* Input callback for receiving structured data */
void input_callback(const void *data, uint16_t len,
                    const linkaddr_t *src, const linkaddr_t *dest)
{
  if(len == sizeof(struct data_form)) {
    struct data_form received;
    memcpy(&received, data, sizeof(received));

    char temp_str[10], hum_str[10];
    double2str(temp_str, received.temp);
    double2str(hum_str, received.hum);

    LOG_INFO("ID=%u | Count=%u | Temp=%s°C | Hum=%s%% from ",
             received.ID, received.count, temp_str, hum_str);
    LOG_INFO_LLADDR(src);
    LOG_INFO_("\n");
  } else {
    LOG_WARN("Unexpected data length: %u bytes\n", len);
  }
}

PROCESS_THREAD(receiver_process, ev, data)
{
  PROCESS_BEGIN();

  LOG_INFO("TelosB MAC address is: ");
  LOG_INFO_LLADDR(&linkaddr_node_addr);
  LOG_INFO_("\n");

  nullnet_set_input_callback(input_callback);

  PROCESS_END();
}
