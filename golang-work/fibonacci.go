/*

*/
package main
import (
    "fmt"
    "os"
    "strconv"
)

func fib(n int) ([]int) {
    li := []int{0,1,1}
    next := 0
    for i:=2;i<n;i++ {
        if i <=2 {
            fmt.Println(li)
        } else {
            next = li[i-2] + li[i-1]
            li = append(li,next)
        }
    }
    return li
}

func main() {
    x,err := strconv.Atoi(os.Args[1])
    if err != nil {
        panic(err)
    }
    fmt.Println(fib(x))
}