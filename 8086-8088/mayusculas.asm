pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    db 256 dup(0) ; Escribir hasta celda 100 con ceros
    cad db "atrml",'$'
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
        ;Load Effective Address
        LEA si, cad ;Direccion del primer caracter
        mov cx, 5 ;Numero de repeticiones
        mayus: 
                mov al, [si]
                sub al, 20h
                mov [si], al
                INC si   ;Adelantar un caracter
                loop mayus

        RET
    Main ENDP
codigo ends
    end Main
    
    