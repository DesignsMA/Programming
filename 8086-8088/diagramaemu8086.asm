pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    db 256 dup(0) ;Escribir hasta celda 100 con ceros
    db 9ah, 5eh, 36h, 0f8h,0dch, 24h  ;datos

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

        mov ax, [100h] ;Indica el segmento y desplazamiento para que calcule la direccion exacta en la memoria
        mov dx, [102h]
        and ah, al
        or dh, dl
        xor ah, dh
        mov al, [104h]
        mov dl, [105h]
        and al, dl
        not al
        or ah, al
        mov [106h], ax
        mov [108h], dx

        RET
    Main ENDP
codigo ends
    end Main
    
    