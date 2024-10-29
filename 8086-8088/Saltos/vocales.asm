pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    cad db 'aeero','$'
    vocales db 'aeiou'
    cas dw dup(0)
    ces dw dup(0)
    cis dw dup(0)
    cos dw dup(0)
    cus dw dup(0)
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
        sig:
            mov al, [si] ; Caracter actual
            CMP al, '$'
            JE fin ;Salta a fin si se llego al final de la cadena
            LEA bx, vocales ;Direccion de vocales
            LEA di, cas ;Direccion del primer contador
            mov cx, 5;  Numero de vocales a contar
            
            esVocal:
                mov ah, [bx] ;mover vocal actual a ah
                CMP al, ah ;Comparar caracter con vocal
                JE cont ; saltar a aumentar contador
                INC di
                INC di ;Siguiente word
                INC bx ;Siguiente vocal
                loop esVocal
            ;Continuar si no se encontro vocal
            INC si ;Siguiente caracter
            JMP sig

        cont:
            mov dx, [di] ;Actualizar contador correspondiente
            INC dx
            mov [di], dx
            INC si ;Mover a siguiente caracter
            JMP sig

        fin:
        RET
    Main ENDP
codigo ends
    end Main
    