def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
    modified_candies = [x + extraCandies for x in candies]
    answer = []
    for x in modified_candies:
        if x == max(candies):
            answer.append('true')
        else:
            answer.append('false')

    return answer

print(kidsWithCandies())