pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    org 200H ;Iniciar en celda 200
    DB 51H, 38H, 95H, 32H, 12H, 00H ;Guardar valores a partir de 0200
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
        
        mov si, 200h
        mov di, 201h
        mov ah, [si]
        mov al, [di]
        add ah, al
        mov di, 202h
        mov al, [di]
        add ah, al
        mov di, 203h
        mov al, [di]
        add ah, al
        mov di, 204h
        mov al, [di]
        add ah, al
        mov di, 205h
        mov [di], ah

        RET
    Main ENDP
codigo ends
    end Main
    
    