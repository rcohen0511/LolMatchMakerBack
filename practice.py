
def twoSum(nums, target):
    numDict = {}
    for num in nums:
        numDict[num] = num

    for num in nums:
        compliment = target - num
        try:
            numDict[compliment]
            if numDict[compliment]:
                solution = [num, numDict[compliment]]
        except:
            solution = None

    return solution

nums = [5, 13, 15, 4]
target = 9

# print(twoSum(nums, target))

def lengthOfLongestSubstring(s):
    i = 0
    longestSub = ""
    while i < len(s):
        j = i +1
        while j < len(s):
            ans = s[i:j]
            if allUnique(ans) and len(ans)>len(longestSub):
                longestSub = ans
            j = j + 1
        i = i + 1
    return(longestSub)

def allUnique(string):
    lookUpTable = {}
    for char in string:
        if lookUpTable.__contains__(char):
            return(False)
        lookUpTable[char] = char
    return(True)

    return()

s = "pwwkew"
# print(lengthOfLongestSubstring(s))

def longestPalindrome(s):
    result = []
    ans = ""
    for i in range(len(s)):
        for j in range(0,i):
            substring = s[j:i+1]
            if isPal(substring):
                result.append(substring)
    for pal in result:
        if len(pal) > len(ans):
            ans = pal
    return (ans)

def isPal(s):
    return s == s[::-1]

s = "forgeeksskeegfor"
# print(longestPalindrome(s))

t = s.replace("for", "abc")
# print(t)

def reverseString(s):
    length = len(s)
    rev = ""

    while length > 0:
        rev += s[length-1]
        length = length -1
    return(rev)

s = "test"
# print(reverseString(s))

def fizzBuzz(n):
    numbers = []
    i = 1
    while n >= i:
        divBy3 = False
        divBy5 = False
        if i%3 == 0:
            divBy3 = True
        if i%5 == 0:
            divBy5 = True
        if divBy3 and divBy5:
            numbers += ["FizzBuzz"]
        elif divBy3:
            numbers += ["Fizz"]
        elif divBy5:
            numbers += ["Buzz"]
        else:
            numbers += [str(i)]
        i = i+1
    return[numbers]

n = 15
# print(fizzBuzz(n))


def singleNumber(nums):
    numberPool = {}


    for num in nums:
        print(numberPool)
        try:
            numberPool.pop(num)
        except:
            numberPool[num] = 1
    return numberPool.popitem()[0]


numbers = [1,6,2,3,3,4,5,5,6,1,7,7,2]
# print(singleNumber(numbers))


def moveZeroes(nums):
    lastNonZeroFound = 0
    length = len(nums)
    for i in range(0,length,1):
        if nums[i] != 0:
            nums[lastNonZeroFound] = nums[i]
            lastNonZeroFound = lastNonZeroFound + 1

    for i in range(lastNonZeroFound, length, 1):
        nums[i] = 0
    return nums

numbers = [0,6,2,0,3,4,0,5,6,1,0,7,2]
print(moveZeroes(numbers))