pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    cad1 DB 'addsdreemplazoaskdareemplazo', '$' 
    ree DB 'palabrare','$'
    pal DB 'reemplazo','$'
    inicio DW 00
datos ends

codigo segment para 'code'
    
   Principal PROC FAR
    assume cs:codigo, ds: datos, ss: pila
    
   push ds
   sub ax,ax
   push ax
   mov ax, datos
   mov ds,ax
   mov es,ax
   
   lea si, pal ;reemplazo
   lea di, cad1 ;original
   mov ah, [si] 
   mov al, [di]
   cmp al, ah ;comparar
   je sig
no: ;si no es  igual
   lea si, pal ; reiniciar reemplazo
   call incremento ;incrementar  si, di,, ah= si, al = di
   je fin       
   cmp ah,al ;si son iguales
   je sig
   jmp no
   
sig:
   mov inicio, di ;guardar inicio
sigletra:
   call incremento ;siguientes caracteres
   cmp ah, al
   jne no ;no son iguales
jmp sigletra
   dec inicio
   lea si, ree
   mov di, inicio
   mov cx, 09H ;
   cld
   rep movsb ;reemplazar de manera  ascendente
   jmp no
     
fin:
   RET

  Principal ENDP
   
Incremento PROC NEAR
    inc si
    inc di
    mov ah, [si]
    mov al, [di]
    ret
Incremento endp
   
  codigo ends
        end Principal
   