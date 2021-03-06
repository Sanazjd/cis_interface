#include <stdio.h>
// Include methods for input/output channels
#include "CisInterface.h"

int main(int argc, char *argv[]) {
  // Initialize input/output channels
  cisPlyInput_t in_channel = cisPlyInput("inputB");
  cisPlyOutput_t out_channel = cisPlyOutput("outputB");

  // Declare resulting variables and create buffer for received message
  int flag = 1;
  ply_t p = init_ply();

  // Loop until there is no longer input or the queues are closed
  while (flag >= 0) {
  
    // Receive input from input channel
    // If there is an error, the flag will be negative
    // Otherwise, it is the size of the received message
    flag = cisRecv(in_channel, &p);
    if (flag < 0) {
      printf("Model B: No more input.\n");
      break;
    }

    // Print received message
    printf("Model B: (%d verts, %d faces)\n", p.nvert, p.nface);
    int i, j;
    printf("  Vertices:\n");
    for (i = 0; i < p.nvert; i++) {
      printf("   %f, %f, %f\n",
	     p.vertices[i][0], p.vertices[i][1], p.vertices[i][2]);
    }
    printf("  Faces:\n");
    for (i = 0; i < p.nface; i++) {
      printf("   %d", p.faces[i][0]);
      for (j = 1; j < p.nvert_in_face[i]; j++)
	printf(", %d", p.faces[i][j]);
      printf("\n");
    }

    // Send output to output channel
    // If there is an error, the flag will be negative
    flag = cisSend(out_channel, p);
    if (flag < 0) {
      printf("Model B: Error sending output.\n");
      break;
    }

  }
  
  // Free dynamically allocated ply structure
  free_ply(&p);
  
  return 0;
}

