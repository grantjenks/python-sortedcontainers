def bubblesort(arr): ## First We Created a Function So that We Dont Need To code repeaditly.
    l=len(arr) ## Calculating The length of List
    for i in range(l-1): ## Here Start The Logic Of Code, Initially l-1 is written because bubble sort will do swap in first loop therefore the largest Element Will Already be At Last, So Last loop Should be One Less
        for j in range(l-1-i):
            if arr[j]>arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
arr=[6,4,5,2,1,7,3]  ## Here i taken An sample Input
bubblesort(arr)   ## You can take Input from USer, Just Change "arr=[6,4,5,2,1,7,3]" with "arr=[int(x) for x in input().split()]"
print(arr)  ## Finally The Sorted list Will be Printed