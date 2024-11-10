pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    cad1 DB '1.SUMA', '$'
    cad2 DB '2.RESTA','$'
    cad3 DB '3.FIN', '$'
    cad4 DB 'Deme una opcion: ','$'
    cad5 DB 'Dame dato 1: ' , '$'
    cad6 DB 'Dame dato 2: ' , '$'
    cad7 DB 'La suma es: ', '$'
    cad8 DB 'La resta es: ' , '$'
    cad9 DB 'Ingrese una opcion valida' , '$'
    cad10 DB 'No se puede realizar la operacion','$'
    opc DB 00
    dato1 DB 00
    dato2 DB 00
    res DB 00 
    
datos ends

codigo segment para 'code'
    
   
   
   MENU1 PROC NEAR
   assume cs:codigo, ds: datos, ss: pila
   
   
menu:

   mov ah, 06
   mov al, 0
   mov bh, 07
   mov cx, 00
   mov dx, 184FH
   int 10H
   
   mov ah, 2
   mov bh, 00
   mov dx, 0000
   int 10H

   lea dx, cad1
   mov ah, 09H
   INT 21H
   
   call renglon
   
   lea dx, cad2
   mov ah, 09H
   INT 21H
   
   call renglon
   
   lea dx, cad3
   mov ah, 09H
   INT 21H
   
   call renglon
   
   lea dx, cad4
   mov ah, 09H
   INT 21H
   
   mov ah, 1
   INT 21H
   
   cmp al, '1'
   jz suma
   cmp al, '2'
   jz resta
   cmp al, '3'
   jz Final
   
   lea dx,cad9
   mov ah, 09H
   int 21H
   jmp menu
   
suma:
   call sum
   jmp menu
   
resta:
   call rest
   jmp menu
   
Final: 
mov ah, 4Ch   ; DOS function to terminate program
    int 21H       ; Terminate and return control to the operating system
   MENU1 endp
   
   sum PROC NEAR
   assume cs:codigo, ds: datos, ss: pila
   
   call renglon
   
   lea dx, cad5
   mov ah, 09H
   int 21H
   
   call renglon
   
   mov ah, 1
   int 21H
   mov res, al
   sub res, 30H
   
   call renglon
   
   lea dx, cad6
   mov ah, 09
   int 21H
   
   call renglon
   
   mov ah, 1
   int 21H
   sub al, 30H
   add res, al
   cmp cl, 0AH
   jge alerta
   cmp cl, 00H
   jle alerta
   
   call renglon
   
   lea dx, cad7
   mov ah, 09
   int 21H
   
   call renglon
   
   add res, 30H
   mov dl, res
   mov ah, 2
   int 21H
   jmp acabo
alerta:
   mov cl, 00
   mov ah, 09H
   lea dx, cad10
   int 21H
   
acabo:
   mov ah, 1
   int 21H
   Ret
   sum endp
   
   rest PROC NEAR
   assume cs:codigo, ds: datos, ss: pila
   
   call renglon
   
   lea dx, cad5
   mov ah, 09H
   int 21H
   
   call renglon
   
   mov ah, 1
   int 21H
   mov res, al
   sub res, 30H
   
   call renglon
   
   lea dx, cad6
   mov ah, 09
   int 21H
   
   call renglon
   
   mov ah, 1
   int 21H
   sub al, 30H
   sub res, al
   cmp res, 0AH
   jge alert
   cmp res, 00H
   jle alert
   
   call renglon
   
   lea dx, cad8
   mov ah, 09
   int 21H
   
   call renglon
   
   mov ah, 2
   add res, 30H
   mov dl, res
   int 21H
   jmp acab
alert:
   call renglon
   mov cl, 00
   mov ah, 09H
   lea dx, cad10
   int 21H
   
acab:
  
   mov ah, 1
   int 21H
   Ret
   rest endp
   
   renglon PROC NEAR
   assume cs:codigo, ds: datos, ss: pila
   
   
   mov ah, 03H
   mov bh, 00
   int 10H
   mov ah, 02H
   mov dl, 00
   inc dh
   int 10H
   
   ret
   
   renglon endp
   
   Principal PROC FAR
    assume cs:codigo, ds: datos, ss: pila
    
    push ds
    sub ax, ax
    mov ax, datos
    mov ds, ax
    mov es, ax
    
    call MENU1
    
    RET
    
   Principal endp 
   codigo ends
    end Principal