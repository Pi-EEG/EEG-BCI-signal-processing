
#define DWT_CONTROL *(volatile unsigned long *)0xE0001000
#define SCB_DEMCR *(volatile unsigned long *)0xE000EDFC


#include "main.h"
SPI_HandleTypeDef hspi3;
TIM_HandleTypeDef htim1;
UART_HandleTypeDef huart5;

void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_UART5_Init(void);
static void MX_SPI3_Init(void);
static void MX_TIM1_Init(void);


char trans_str[64] = {0,};
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim) // колбек по захвату
	 	  {
		          if(htim->Instance == TIM1)
	 	          {
	 	                  if(htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1)
	 	                  {
	 	                          __HAL_TIM_SET_COUNTER(&htim1, 0x0000);
	 	                  }
	 	                  else if(htim->Channel == HAL_TIM_ACTIVE_CHANNEL_2)
	 	                  {
	 	                          uint32_t falling = HAL_TIM_ReadCapturedValue(&htim1, TIM_CHANNEL_2);
	 	                          // чтение значени�? в реги�?тре захвата/�?равнени�?
	 	                          snprintf(trans_str, 63, "Pulse %lu mks\n", falling);
	 	                          HAL_UART_Transmit(&huart5, (uint8_t*)trans_str, strlen(trans_str), 1000);
	 	                  }
	 	          }
	 	  }




int main(void)
{

  HAL_Init();
  SystemClock_Config();
  MX_GPIO_Init();
  MX_UART5_Init();
  MX_SPI3_Init();

  MX_TIM1_Init();




   int received_byte;
   uint8_t SDATAC = 0x11;
   uint8_t RESET = 0x06;
 //  uint8_t WAKEUP = 0x02;

   uint8_t CONFIG1 = 0x01;
   uint8_t CONFIG2 = 0x02;
   uint8_t CONFIG3 = 0x03;
   uint8_t START = 0x08;
   uint8_t test = 0x00;
   uint8_t RDATAC = 0x10;
  // uint8_t STOP = 0x0a;

   uint8_t CH1SET = 0x05;
   uint8_t CH2SET = 0x06;
   uint8_t CH3SET = 0x07;
   uint8_t CH4SET = 0x08;
   uint8_t CH5SET = 0x09;
   uint8_t CH6SET = 0x0A;
   uint8_t CH7SET = 0x0B;
   uint8_t CH8SET = 0x0C;

   uint8_t received_Byte;
   uint32_t output[9]= {0};

   uint32_t result_collect [9]= {0};

   uint32_t dataPacket;
   uint32_t dataPacket_3bytes;



   uint32_t data_test = 0x7FFFFF;
   uint32_t data_check = 0xFFFFFF;

   uint32_t result;
   uint32_t result_before;
   int average_result_massiv[10]={0};
   int average_result;

   uint32_t noise_massive [100]={0};
   uint32_t final_noise_massive [100]={0};
   uint32_t summa_noise;
   int zad = 8;
   int i_count = 0;
   int average_count= 0;
   int chanel_num =0;




	void DWT_Init(void)
	{
	    SCB_DEMCR |= CoreDebug_DEMCR_TRCENA_Msk; // разрешаем использовать счётчик
	    DWT_CONTROL |= DWT_CTRL_CYCCNTENA_Msk;   // запускаем счётчик
	}


	DWT_Init();

//#define DWT_CONTROL *(volatile unsigned long *)0xE0001000
//#define SCB_DEMCR *(volatile unsigned long *)0xE000EDFC
//  	  void DWT_Init(void)
//  	  {
/////  	      SCB_DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
  	   //   DWT_CONTROL |= DWT_CTRL_CYCCNTENA_Msk;
  //	  }
  //	void delay_us(uint32_t us)
  //	{
  //	    uint32_t us_count_tic =  us * (SystemCoreClock / 1000000);
  //	    DWT->CYCCNT = 0U;
  //	    while(DWT->CYCCNT < us_count_tic);
  ////	}
  //	DWT_Init();




   void send_data_to_brainflow (result)        {



        int y = 255;
        char first_byte = result >> 16;





        int second_byte_int = (result >> 8) & y;
        unsigned char  second_byte = second_byte_int;

        int third_byte_int = result & y;
        unsigned char  third_byte =  third_byte_int;

   HAL_UART_Transmit(&huart5, (uint8_t*)&first_byte, 1, 10);
   HAL_UART_Transmit(&huart5, (uint8_t*)&second_byte, 1, 10);
   HAL_UART_Transmit(&huart5, (uint8_t*)&third_byte, 1, 10);

                                                }



  void send_command(uint8_t cmd)
  	    {
  	  		    HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_RESET);
  	  	        HAL_SPI_Transmit(&hspi3, (uint8_t*)&cmd,1, 0x1000);
  	  	        HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_SET);
  	  	  }


  	  void send_data_by_uart (received_byte)
  	  	  {
  	  	  // step 1 - convert dataset
  	  	  char buffer[16];
  	  	  char buffer1[16];
  	  	  sprintf(buffer1, "%d\n", received_byte);
  	      int a=0;
  	  	  for (a; a<strlen(buffer1); a=a+1) //
  	  	         {
  	  		   if (buffer1[a]!= 0)
  	  		   	        	      {
  	  		   buffer[0] = buffer1[a];
              //  uint8_t  ildaron = 1;
  	  		   HAL_UART_Transmit(&huart5, buffer, 1, 1000);

  	  	                          }
  	  	          }
  	             a=0;
  	  	  }


  	void send_data_by_uart_esp1 ()
  	  	  	  {
  		  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_11,GPIO_PIN_RESET);
	  	  char buffer[16];
	  	 // char buffer7[]="AT+CWMODE=1\n";
	  	char buffer7[]="AT+CWMODE=1\r\n";
	      int a=0;
	  	  for (a; a<strlen(buffer7); a=a+1) //
	  	         {
	  		   buffer[0] = buffer7[a];
	  		   HAL_UART_Transmit(&huart5, buffer, 1, 1000);
	  	          }
	             a=0;
	         HAL_Delay(6000);

    	  	  	  char buffer0[]="AT+CWJAP=\"HUAWEI nova lite 3\",\"bender123\"\r\n";
    	  	  	 // char buffer0[]="AT+CWJAP=\"HUAWEI nova lite 3\",\"bender123\"\n";
    	  	  	  for (a; a<strlen(buffer0); a=a+1) //
    	  	  	         {
    	  	  		   buffer[0] = buffer0[a];
    	  	  		   HAL_UART_Transmit(&huart5, buffer, 1, 1000);
    	  	  	          }
    	  	             a=0;
    	  	         HAL_Delay(6000);


  	  	  	  // step 1 - convert dataset
  	  	  	  char buffer1[]="AT+CIPMODE=0\r\n";
  	  	  	  for (a; a<strlen(buffer1); a=a+1) //
  	  	  	         {
  	  	  		   buffer[0] = buffer1[a];
  	  	  		   HAL_UART_Transmit(&huart5, buffer, 1, 1000);
  	  	  	          }
  	  	             a=0;
  	  	         HAL_Delay(1000);


  	   	  	  	 // char buffer[16];
  	   	  	  	  char buffer2[]="AT+CIPMUX=1\r\n";
  	   	  	     // int a=0;
  	   	  	  	  for (a; a<strlen(buffer2); a=a+1) //
  	   	  	  	         {
  	   	  	  		   buffer[0] = buffer2[a];
  	   	  	  		   HAL_UART_Transmit(&huart5, buffer, 1, 1000);
  	   	  	  	          }
  	   	  	             a=0;
  	   	  	      HAL_Delay(1000);
  	   	  	  	  	  char buffer3[]="AT+CIPSERVER=1,49667\r\n";
  	   	  	  	  	  for (a; a<strlen(buffer3); a=a+1) //
  	   	  	  	  	         {
  	   	  	  	  		   buffer[0] = buffer3[a];
  	   	  	  	  		   HAL_UART_Transmit(&huart5, buffer, 1, 1000);
  	   	  	  	  	          }
  	   	  	  	             a=0;
  	   	  	  	    HAL_Delay(1000);

  	  	  	  }


  	void send_data_by_uart_esp2 (voltage_value)
  	  	  	  {
  		                      int a=0;
  		                      char buffer[16];
  	                          char buffer4[]="AT+CIPSEND=0,5\r\n";
  	  	   	    	  	  	  for (a; a<strlen(buffer4); a=a+1) //
  	  	   	    	  	  	         {
  	  	   	    	  	  		   buffer[0] = buffer4[a];
  	  	   	    	  	  		   HAL_UART_Transmit(&huart5, buffer, 1, 1000);
  	  	   	    	  	  	          }
  	  	   	    	  	             a=0;
  	  	   	    	  	          HAL_Delay(5);
  	  	   	    	  	          char buffer5[16];
  	  	   	    	  	          sprintf(buffer5, "%d\r\n", voltage_value);
  	  	   	    	  	  	  	 // char buffer5[]="ildar\r\n";
  	  	   	    	  	  	  	  for (a; a<strlen(buffer5); a=a+1) //
  	  	   	    	  	  	  	         {
  	  	   	    	  	  	  		   buffer[0] = buffer5[a];
  	  	   	    	  	  	  		   HAL_UART_Transmit(&huart5, buffer, 1, 1000);

  	  	   	    	  	  	  	          }
  	  	   	    	  	  	             a=0;
  	  	   	    	  	  	    HAL_Delay(5);
  	  	  	  }


  	 HAL_Delay(1000);

  	    void write_byte(uint8_t reg_addr, uint8_t val_hex)
  	    {
  	     HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_RESET);
  	     uint8_t adress = 0x40|reg_addr;
  	     HAL_SPI_Transmit(&hspi3, (uint8_t*)&adress, 1, 0x1000);
  	     HAL_SPI_Transmit(&hspi3, (uint8_t*)&test, 1, 0x1000);
  	     HAL_SPI_Transmit(&hspi3, (uint8_t*)&val_hex, 1, 0x1000);
    	 HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_SET);
  	    }

  	    uint8_t read_byte(uint8_t reg_addr)
  	    {
  	      uint8_t out;

  	      HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_RESET);
  	      uint8_t adress = 0x20 | reg_addr ;  //
  	      HAL_SPI_Transmit(&hspi3, (uint8_t*) &adress, 1 ,0x1000);
  	      HAL_SPI_Transmit(&hspi3, (uint8_t*)&test, 1, 0x1000);
  	     // HAL_SPI_Receive(&hspi3, (uint8_t*)&out,1, 0x1000);
  	      HAL_SPI_TransmitReceive(&hspi3,(uint8_t*)&test,(uint8_t*)&out,1,0x1000);
  	      HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_SET);
    	  return(out);
  	    }

  	    void live_bits ()
  	    {
  	      HAL_Delay(100);
  	      HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_10);
  	      HAL_Delay(100);
  	    }

       int measure_noise()
       {
    	   summa_noise=0;
           int zad = 8;
    	   uint32_t noise_massive [100]={0};
  	       write_byte(CH1SET, 0x01);
    	   for (int count = 0; count<100; count++){

    	   if (HAL_GPIO_ReadPin(DRDY_GPIO_Port, DRDY_Pin) == GPIO_PIN_SET)
    	                         {
    	  	              zad = 5;
    	                         }
    	   	    	if (HAL_GPIO_ReadPin(DRDY_GPIO_Port, DRDY_Pin) == GPIO_PIN_RESET && zad==5){

    	   	    		        zad=0;
    	   	    	            HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_RESET);
    	   	    	            for(int i = 0; i<9; i++){
    	   	    	            	dataPacket = 0;
    	   	    	                for(int j = 0; j<3; j++){
    	   	    	                    HAL_SPI_TransmitReceive(&hspi3,(uint8_t*)&test,&received_Byte,1,0x1000);
    	   	    	                    dataPacket = (dataPacket<<8)|received_Byte;

    	   	    	                }
    	   	    	                output[i] = dataPacket;
    	   	    	                dataPacket = 0;
    	   	    	            }
    	   	    	             result_before = output[1]|data_test;
    	   	    	             if (result_before==data_check)
    	  		                 {
    	   	    	            	noise_massive[count] = 16777214-output[1];
    	   	    	            //	send_data_by_uart(noise_massive[count]);
    	  		                 }
    	  		                  else
    	  		                  {
    	  		                	noise_massive[count] = output[1];
    	  		               // 	send_data_by_uart(noise_massive[count]);
    	  		                  }
    	   	    	            if (i_count==100)
    	   	    	            {
    	   	    	            i_count=0;
    	   	    	            for ( int ir_count = 0; ir_count < 100; ir_count++) {
    	   	    	           	          summa_noise += final_noise_massive[ir_count];
    	   	    	          	   }
    	   	    	               summa_noise=summa_noise/100;
    	   	    	               send_data_by_uart (summa_noise);
    	   	    	               }
    	   	    	      //     send_data_by_uart (i_count);
    	   	    	      //     send_data_by_uart (noise_massive[count]);
    	   	    	           final_noise_massive[i_count]=noise_massive[count];
    	   	    	           i_count++;
              }
              }
       }


       int measure_impedance()
	   {
    	 write_byte(CH1SET, 0x00);
	 	 write_byte(0x0D, 0x00);    // 0F  BIAS_SENSP: Bias Drive Positive Derivation Register
	 	 write_byte(0x0E, 0x00);    // 0F  BIAS_SENSN: Bias Drive Negative Derivation Register
	 	 write_byte(0x0F, 0x01);  // LOFF_SENSP: Positive Signal Lead-Off Detection Register
       }

       int measure_standart()
       {

       }
  	   HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_SET);

  	                                    send_command(SDATAC);
  	   	    	 	  	                HAL_SPI_Transmit(&hspi3, (uint8_t*)&RESET, 1, 0x1000);
  	   	    	 	      	            HAL_Delay(1000);
  	   	    	 	    	 	        write_byte(CONFIG1, 0xB6); // 96
  	   	    	 	   	 	            write_byte(CONFIG2, 0xD4);  //D3
  	   	    	 	   	 	            write_byte(CONFIG3, 0xE0); // EC

  	   	    	 	   	 	            write_byte(0x04, 0x00);  // not all

  	   	    	 	   	 	            write_byte(0x0D, 0xFF); // 0F  BIAS_SENSP: Bias Drive Positive Derivation Register
  	   	    	 	   	 	            write_byte(0x0E, 0x00); // 0F  BIAS_SENSN: Bias Drive Negative Derivation Register

  	   	    	 	   	 	            write_byte(0x0F, 0x00);  // LOFF_SENSP: Positive Signal Lead-Off Detection Register

  	   	    	 	   	 	            write_byte(0x10, 0x00);  // LOFF_SENSN: Negative Signal Lead-Off Detection Register
  	   	    	 	   	 	            write_byte(0x11, 0x00);  // LOFF_FLIP: Lead-Off Flip Register
   	   	    	 	   	 	          //  write_byte(0x12, 0x00);  // (Read-Only) LOFF_STATP: Lead-Off Positive Signal Status Register
   	  	    	 	   	 	          //  write_byte(0x13, 0x00);  // (Read-Only)LOFF_STATN: Lead-Off Negative Signal Status Register
   	   	    	 	   	 	            write_byte(0x14, 0x80);  // gpio  OF
   	   	    	 	   	 	            write_byte(0x15, 0x20);  // MISC1


   	   	    	 	   	 	        //  write_byte(0x16, 0x00); // RESERVED
   	   	    	 	   	 	            write_byte(0x17, 0x00);  // CONFIG4

  	   	    	 	    	  	     write_byte(CH1SET, 0x40); // 68
  	   	    	 	    	 	     write_byte(CH2SET, 0x01); //
  	   	    	 	    	 	     write_byte(CH3SET, 0x01); //
  	   	    	 	    	 	     write_byte(CH4SET, 0x01); //
  	   	    	 	    	 	     write_byte(CH5SET, 0x01); //
  	   	    	 	    	 	     write_byte(CH6SET, 0x01); //
  	   	    	 	    	 	     write_byte(CH7SET, 0x01); //
  	   	    	 	    	 	     write_byte(CH8SET, 0x01); //

  	   	    	 	    	       // 	 write_byte(0x0D, 0x00);
  	   	    	 	    	       // 	 write_byte(0x0E, 0x00);

  	   	    	 	    	 	//    HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_SET);

  	   	    	 	    	        // send_command(RDATAC);
  	   	    	 	    	 	    // delay_us(150);
  	   	    	 	                // HAL_GPIO_WritePin(GPIOD, START_Pin, GPIO_PIN_RESET);
  	   	    	 	    	 	   send_command(SDATAC);
  	   	    	 	    	 	   uint8_t read_reg = read_byte(CH1SET);
 	    	 	     	   	 	//   send_data_by_uart(read_reg);
  	   	    	 	     	   	   HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_SET);

  	   	    	 	     	   	 	    	  	     //HAL_GPIO_WritePin(GPIOD, START_Pin, GPIO_PIN_RESET);

                                   HAL_Delay(1000);

                       //         HAL_GPIO_WritePin(GPIOD, START_Pin, GPIO_PIN_SET);
                      //          send_command(START);

                        //        HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_RESET);
  	   	                        send_command(RDATAC);
  	   	    	 	 	        HAL_Delay(1);
  	   	                        send_command(START);

  	   	    	 	 	        HAL_Delay(1);
  	   	    	 	 	     //   send_command(RDATAC);
  	   	    	 	 	    //   HAL_SPI_Transmit(&hspi3, (uint8_t*)&START,1, 0x1000);
  	   	    	 	 	 //      HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_RESET);
  	   	    	 	 	      //  delay_us(50);
  	   	    	 	 	      //  send_command(RDATAC);
  	   	    	 	 	   //    HAL_SPI_Transmit(&hspi3, (uint8_t*)&RDATAC,1, 0x1000);
  	   	    	 	      //	 delay_us(5);
  	   	    	 	      //     HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_SET);

HAL_GPIO_WritePin(GPIOB, GPIO_PIN_11,GPIO_PIN_SET);
HAL_GPIO_WritePin(GPIOB, GPIO_PIN_10,GPIO_PIN_SET);

//send_data_by_uart_esp1();
int only_1_times=0;
HAL_Delay(500);

unsigned char sample_number=0;
uint8_t start_command_receive[1]= {0};

int step;
step =0;

HAL_GPIO_WritePin(GPIOD, CS2_Pin, GPIO_PIN_SET);
//HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_SET);

HAL_TIM_Base_Start_IT(&htim1);

HAL_TIM_IC_Start_IT(&htim1, TIM_CHANNEL_1);
HAL_TIM_IC_Start_IT(&htim1, TIM_CHANNEL_2);



 	      while (1)
  {


 	    	      //    HAL_GPIO_WritePin(GPIOE, GPIO_PIN_10, GPIO_PIN_SET);
 	    	      //    HAL_Delay(320); // длина импульса
 	    	      //    HAL_GPIO_WritePin(GPIOE, GPIO_PIN_10, GPIO_PIN_RESET);
 	    	       //   HAL_Delay(20);


 	    	if (HAL_GPIO_ReadPin(DRDY_GPIO_Port, DRDY_Pin) == GPIO_PIN_SET)
 	    	                         {
 	    	  	              zad = 5;
 	    	                         }

 	    	if (HAL_GPIO_ReadPin(DRDY_GPIO_Port, DRDY_Pin) == GPIO_PIN_RESET && zad==5 ){ //


 	    	  	          int time1=1;
 	    	              send_data_by_uart(time1);

 	    		        zad = 0;
 	    	            HAL_GPIO_WritePin(GPIOD, CS_Pin, GPIO_PIN_RESET);

 	    	            //Time_1
 	    	            HAL_GPIO_WritePin(GPIOE, GPIO_PIN_10, GPIO_PIN_SET);

 	    	            for(int i = 0; i<9; i++){
 	    	            	dataPacket = 0;
 	    	                for(int j = 0; j<3; j++){
 	    	                    HAL_SPI_TransmitReceive(&hspi3,(uint8_t*)&test,&received_Byte,1,0x1000);
 	    	                    dataPacket = (dataPacket<<8)|received_Byte;
 	    	                }

 	    	                output[i] = dataPacket;
 	    	                dataPacket = 0;
 	    	                }
 	    	              HAL_GPIO_WritePin(GPIOE, GPIO_PIN_10, GPIO_PIN_RESET);

 	    	        	  int time2=2;
 	    	              send_data_by_uart(time2);
 	    	           //Time_2
 	    	            HAL_GPIO_WritePin(GPIOE, GPIO_PIN_10, GPIO_PIN_SET);

 	    	            for (chanel_num=0; chanel_num<9; chanel_num++){  //6

 	    	            result_before = output[chanel_num]|data_test;
 	    	            if (result_before==data_check)
		               {
		            	   result_collect[chanel_num] = (16777214-output[chanel_num]); // -864//*((2*4.5)/16777215);
		                 //  send_data_by_uart(result);
 	    	           }
		                  else
		                  { //LSB = (2 x VREF) // Gain / (2 ^ 24 - 1)
		                	  result_collect[chanel_num] = output[chanel_num]; //-864//*((2*4.5)/16777215);//
		                  }
 	    	                                                           }

                          //Time_3

                          // start second part

 	    	              send_data_by_uart( result_collect[1]);
 	    	              send_data_by_uart( result_collect[2]);
 	    	              send_data_by_uart( result_collect[3]);
 	    	              send_data_by_uart( result_collect[4]);
 	    	              send_data_by_uart( result_collect[5]);
 	    	              send_data_by_uart( result_collect[6]);
 	    	              send_data_by_uart( result_collect[7]);
 	    	              send_data_by_uart( result_collect[8]);


 	    	              HAL_GPIO_WritePin(GPIOE, GPIO_PIN_10, GPIO_PIN_RESET);

 	    	              int y = 255;
 	    	              char first_byte = result >> 16;

 	    	              int second_byte_int = (result >> 8) & y;
 	    	              unsigned char  second_byte = second_byte_int;

 	    	              int third_byte_int = result & y;
 	    	              unsigned char  third_byte =  third_byte_int;

                          unsigned char byte_0 = 160;
                          unsigned char byte_26 = 192;

                          char start_command [] =  "b";



                          if( HAL_UART_Receive(&huart5, (uint8_t*)start_command_receive, 1, 1) == HAL_OK )
                       //   HAL_UART_Receive(&huart5, (uint8_t*)start_command_receive, 1, 1000);
                          {
                          if (start_command_receive[0] == 98) {
                        	  step=888;
                          }
                          if (start_command_receive[0] == 99) {
                              step=0;
                              //sample_number=0;
                                                  }
                          }
                          if (step == 888)
	                                                   {
                          sample_number = sample_number+1;

                          HAL_UART_Transmit(&huart5, (uint8_t*)&byte_0, 1, 1);
                          HAL_UART_Transmit(&huart5, (uint8_t*)&sample_number, 1, 10);


                          send_data_to_brainflow ( result_collect[1]);
                          send_data_to_brainflow ( result_collect[2]);
                          send_data_to_brainflow ( result_collect[3]);
                          send_data_to_brainflow ( result_collect[4]);

                          send_data_to_brainflow ( result_collect[1]);
                          send_data_to_brainflow ( result_collect[2]);
                          send_data_to_brainflow ( result_collect[3]);
                          send_data_to_brainflow ( result_collect[4]);

                     //     HAL_UART_Transmit(&huart5, (uint8_t*)&first_byte, 1, 10);
                      //    HAL_UART_Transmit(&huart5, (uint8_t*)&second_byte, 1, 10);
                      //    HAL_UART_Transmit(&huart5, (uint8_t*)&third_byte, 1, 10);

                      //    HAL_UART_Transmit(&huart5, (uint8_t*)&first_byte, 1, 10);
                      //    HAL_UART_Transmit(&huart5, (uint8_t*)&second_byte, 1, 10);
                       //   HAL_UART_Transmit(&huart5, (uint8_t*)&third_byte, 1, 10);

                     //     HAL_UART_Transmit(&huart5, (uint8_t*)&first_byte, 1, 10);
                    //      HAL_UART_Transmit(&huart5, (uint8_t*)&second_byte, 1, 10);
                    //      HAL_UART_Transmit(&huart5, (uint8_t*)&third_byte, 1, 10);

                    //      HAL_UART_Transmit(&huart5, (uint8_t*)&first_byte, 1, 10);
                    //      HAL_UART_Transmit(&huart5, (uint8_t*)&second_byte, 1, 10);
                   //       HAL_UART_Transmit(&huart5, (uint8_t*)&third_byte, 1, 10);

                    //      HAL_UART_Transmit(&huart5, (uint8_t*)&first_byte, 1, 10);
                    //      HAL_UART_Transmit(&huart5, (uint8_t*)&second_byte, 1, 10);
                    //      HAL_UART_Transmit(&huart5, (uint8_t*)&third_byte, 1, 10);

                     //     HAL_UART_Transmit(&huart5, (uint8_t*)&first_byte, 1, 10);
                    //      HAL_UART_Transmit(&huart5, (uint8_t*)&second_byte, 1, 10);
                     //     HAL_UART_Transmit(&huart5, (uint8_t*)&third_byte, 1, 10);

                     //     HAL_UART_Transmit(&huart5, (uint8_t*)&first_byte, 1, 10);
                     //     HAL_UART_Transmit(&huart5, (uint8_t*)&second_byte, 1, 10);
                     //     HAL_UART_Transmit(&huart5, (uint8_t*)&third_byte, 1, 10);

                       //   HAL_UART_Transmit(&huart5, (uint8_t*)&first_byte, 1, 10);
                       //   HAL_UART_Transmit(&huart5, (uint8_t*)&second_byte, 1, 10);
                      //   HAL_UART_Transmit(&huart5, (uint8_t*)&third_byte, 1, 10);

                          HAL_UART_Transmit(&huart5, (uint8_t*)&byte_26, 1, 10);

	                                                   }
            // HAL_Delay (5);
 	    	 }

   }
}





void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage 
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV2;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief SPI3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI3_Init(void)
{

  /* USER CODE BEGIN SPI3_Init 0 */

  /* USER CODE END SPI3_Init 0 */

  /* USER CODE BEGIN SPI3_Init 1 */

  /* USER CODE END SPI3_Init 1 */
  /* SPI3 parameter configuration*/
  hspi3.Instance = SPI3;
  hspi3.Init.Mode = SPI_MODE_MASTER;
  hspi3.Init.Direction = SPI_DIRECTION_2LINES;
  hspi3.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi3.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi3.Init.CLKPhase = SPI_PHASE_2EDGE;
  hspi3.Init.NSS = SPI_NSS_SOFT;
  hspi3.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_16;
  hspi3.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi3.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi3.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi3.Init.CRCPolynomial = 10;
  if (HAL_SPI_Init(&hspi3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI3_Init 2 */

  /* USER CODE END SPI3_Init 2 */

}


/**
  * @brief TIM1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{

  /* USER CODE BEGIN TIM1_Init 0 */

  /* USER CODE END TIM1_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_IC_InitTypeDef sConfigIC = {0};

  /* USER CODE BEGIN TIM1_Init 1 */

  /* USER CODE END TIM1_Init 1 */
  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 8;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 600;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_IC_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
  sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;
  sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;
  sConfigIC.ICFilter = 0;
  if (HAL_TIM_IC_ConfigChannel(&htim1, &sConfigIC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_FALLING;
  sConfigIC.ICSelection = TIM_ICSELECTION_INDIRECTTI;
  if (HAL_TIM_IC_ConfigChannel(&htim1, &sConfigIC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */

}






/**
  * @brief UART5 Initialization Function
  * @param None
  * @retval None
  */
static void MX_UART5_Init(void)
{

  /* USER CODE BEGIN UART5_Init 0 */

  /* USER CODE END UART5_Init 0 */

  /* USER CODE BEGIN UART5_Init 1 */

  /* USER CODE END UART5_Init 1 */
  huart5.Instance = UART5;
  huart5.Init.BaudRate = 115200 ;// 115200
  huart5.Init.WordLength = UART_WORDLENGTH_8B;
  huart5.Init.StopBits = UART_STOPBITS_1;
  huart5.Init.Parity = UART_PARITY_NONE;
  huart5.Init.Mode = UART_MODE_TX_RX;
  huart5.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart5.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart5) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN UART5_Init 2 */

  /* USER CODE END UART5_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOE_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_0, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOE, GPIO_PIN_15, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOE, GPIO_PIN_10, GPIO_PIN_RESET);
  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_10|GPIO_PIN_11, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOD, START_Pin|CS_Pin|CS2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : PA0 */
  GPIO_InitStruct.Pin = GPIO_PIN_0;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : PE15 */
  GPIO_InitStruct.Pin = GPIO_PIN_15|GPIO_PIN_10;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);

  /*Configure GPIO pins : PB10 PB11 */
  GPIO_InitStruct.Pin = GPIO_PIN_10|GPIO_PIN_11;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pins : START_Pin CS_Pin */
  GPIO_InitStruct.Pin = START_Pin|CS_Pin|CS2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

  /*Configure GPIO pin : DRDY_Pin */
  GPIO_InitStruct.Pin = DRDY_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(DRDY_GPIO_Port, &GPIO_InitStruct);

}
//g









void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
