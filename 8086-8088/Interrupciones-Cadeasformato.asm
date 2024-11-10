pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    cad db "Hola", '$'

datos ends

codigo segment para 'code'
    Main PROC FAR
        assume cs:codigo, ds:datos, ss:pila
        ; Protocolo
        push ds
        sub ax,ax
        push ax
        mov ax, datos
        mov ds, ax
        mov es, ax
        ; - 
        ;   Back     Fore
        ;BL R G B I R G B
        ;0  0 0 1 0 0 0 0
        ;7  6 5 4 3 2 1 0
        
    
        mov bh, 0
        mov dh, 5
        mov dl, 40
        mov ah, 2
        INT 10h

        LEA si, cad
        mov bl, 24 ; fondo azul con intensidad 1
        mov cx, 1; repetir una vez
        imprimir:
            mov ah, 9
            mov al, [si] ; Caracter
            cmp al, '$' ;salir
            JE salir
            INT 10h

            INC si
            INC dl ; Columna
            add bl, 2 ; Colores intercalados
            mov ah, 2
            INT 10h

            cmp bl, 00011111b ; 1FH
            JG reiniciar
            JMP imprimir

        reiniciar:
            mov bl, 18h; Reiniciando a: 0  0 0 0 0 0 0 1
            JMP imprimir

        salir:
            RET
    Main ENDP
codigo ends
    end Main
     
    