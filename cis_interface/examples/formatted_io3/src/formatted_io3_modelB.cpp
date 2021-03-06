#include <iostream>
// Include methods for input/output channels
#include "CisInterface.hpp"

#define MYBUFSIZ 1000

int main(int argc, char *argv[]) {
  // Initialize input/output channels
  CisAsciiArrayInput in_channel("inputB");
  CisAsciiArrayOutput out_channel("outputB", "%6s\t%d\t%f\n");

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
    flag = in_channel.recv(3, &name, &count, &size);
    if (flag < 0) {
      std::cout << "Model B: No more input." << std::endl;
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
    flag = out_channel.send(3, nrows, name, count, size);
    if (flag < 0) {
      std::cout << "Model B: Error sending output." << std::endl;
      break;
    }

  }
  
  // Free dynamically allocated columns
  if (name) free(name);
  if (count) free(count);
  if (size) free(size);
  
  return 0;
}
