#include <stdio.h>
// Include methods for input/output channels
#include "CisInterface.h"

int main(int argc, char *argv[]) {
  // Initialize input/output channels
  cisAsciiArrayInput_t in_channel = cisAsciiArrayInput("inputA");
  cisAsciiArrayOutput_t out_channel = cisAsciiArrayOutput("outputA", "%6s\t%d\t%f\n");

  // Declare resulting variables and create buffer for received message
  int flag = 1;
  char *name = NULL;
  int *count = NULL;
  double *size = NULL;

  // Loop until there is no longer input or the queues are closed
  while (flag >= 0) {
  
    // Receive input from input channel
    // If there is an error, the flag will be negative
    // Otherwise, it is the size of the received message
    flag = cisRecv(in_channel, &name, &count, &size);
    if (flag < 0) {
      printf("Model A: No more input.\n");
      break;
    }

    // Print received message
    int nrows = flag;
    printf("Model A: (%d rows)\n", nrows);
    int i;
    for (i = 0; i < nrows; i++)
      printf("   %.6s, %d, %f\n", &name[6*i], count[i], size[i]);

    // Send output to output channel
    // If there is an error, the flag will be negative
    flag = cisSend(out_channel, nrows, name, count, size);
    if (flag < 0) {
      printf("Model A: Error sending output.\n");
      break;
    }

  }

  // Free dynamically allocated columns
  if (name) free(name);
  if (count) free(count);
  if (size) free(size);
  
  return 0;
}

