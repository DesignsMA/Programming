pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    nums db 7,2

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

        LEA si, nums
        mov cx, [si]
        add ch, cl
        add ch, 30h
        mov bh, 0 ;Pagina
        mov dh, 15 ;Renglon
        mov dl, 30 ;Columna
        mov ah, 2 ; Servicio
        INT 10h ; Interrupcion

        mov dl, ch
        INT 21h
        RET
    Main ENDP
codigo ends
    end Main
    
    