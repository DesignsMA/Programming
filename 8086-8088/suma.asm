pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    org 100h
    db 97h, 0e2h, 83h, 0c7h   ;datos

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

        mov ax, [ds:100h]
        mov dx, [ds:102h]
        add ah, al
        add dh, dl
        add ah, dh
        mov [ds:105h], ah

        RET
    Main ENDP
codigo ends
    end Main
    
    