#include <stdio.h>
#include <stdlib.h>
#include <gmp.h>

int main(void){
  mpf_t ldPI;
  mp_exp_t mp_exponent;
  char* sOut;
  mpf_init (ldPI);
  mpf_set_si(ldPI,3.14156);

  puts("Vemos el flotante...");
  sOut=mpf_get_str(NULL,&mp_exponent,10,30,ldPI);
  puts(sOut);
  puts("End...");

  free(sOut);
  mpf_clear(ldPI);

  do
  {
    printf("\na");
  } while( getchar() != 'a');
  
  return 0;
}