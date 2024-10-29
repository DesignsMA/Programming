pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    cad db 'ala','$'
    conta dw dup(0)
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

        LEA si, cad ;Guardar direccion
        LEA di, conta
        mov dx, 0
        siguiente:
            mov al, [si] ; Caracter actual
            CMP al, '$'
            JE fin ;Salta a fin si es igual
            CMP al, 'a'
            JE contarA
            INC si
            JMP siguiente
        contarA:
        INC dx
        INC si
        JMP siguiente

        fin:
        mov [di],dx
        RET
    Main ENDP
codigo ends
    end Main
    