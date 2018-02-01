#include <stdio.h>
#include "PsiInterface.h"

int main() {
  int ret = 0;
  int bufsiz = 512;
  char *buf = (char*)malloc(bufsiz);
  
  printf("Hello from C pipe_dst\n");

  // Ins/outs matching with the the model yaml
  psiInput_t inq = psiInput("input_pipe");
  psiOutput_t outf = psiOutput("output_pipe");
  printf("pipe_dst(C): Created I/O channels\n");

  // Continue receiving input from the queue
  int count = 0;
  while (1) {
    ret = psi_recv_nolimit(inq, &buf, bufsiz);
    if (ret < 0) {
      printf("pipe_dst(C): Input channel closed\n");
      break;
    }
    if (ret > bufsiz) {
      printf("pipe_dst(CPP): Buffer increased to %d bytes\n", bufsiz);
      bufsiz = ret;
    }
    ret = psi_send_nolimit(outf, buf, bufsiz);
    if (ret < 0) {
      printf("pipe_dst(C): END ERROR ON MSG %d\n", count);
      free(buf);
      return -1;
    }
    count++;
  }

  printf("Goodbye from C destination. Received %d messages\n", count);

  free(buf);
  return 0;
}

