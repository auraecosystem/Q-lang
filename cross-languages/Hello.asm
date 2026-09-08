.model small
.stack 100h

.data
    message db 'Hello, World!$'

.code
main proc
    mov ax, @data
    mov ds, ax

    mov dx, offset message
    mov ah, 09h
    int 21h

    mov ax, 4C00h
    int 21h
main endp

end main
