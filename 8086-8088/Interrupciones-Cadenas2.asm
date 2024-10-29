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

        mov bh, 0
        mov dh, 5
        mov dl, 40
        mov ah, 2
        INT 10h
        LEA si, cad
        imprimir:
            mov dl, [si]
            cmp dl, '$'
            JE salir
            INT 21h
            INC si
            JMP imprimir
        
        salir:
        RET
    Main ENDP
codigo ends
    end Main
