def insertionsort(arr):  ## here First Creating A Function So no need of repeatation Of Code.
    l=len(arr) ## Calculated Length for comparing Elements of List And Swap 
    for i in range(1,l): ## this is Basic Logic
        j=i-1
        temp=arr[i]
        while (j>=0 and arr[j] >temp):
            arr[j+1]=arr[j]
            j-=1
        arr[j+1] =temp
arr=[9,8,5,6,7,1] ## Rahter Than This Take Input Form User, Just change "arr=[9,8,5,6,7,1]" with "arr=[int(x) for x in input().split()]"
insertionsort(arr)
print(arr)## Final Sorted List is Printed