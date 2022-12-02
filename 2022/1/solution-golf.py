# more an exercise in making things ugly than in size.
# expects input numbers to be in a file called `g`.
print(max(sum(int(i)for i in l.strip().split("\n"))for l in open("g","r").read().split("\n\n")))
print(sum(sorted((sum(int(i)for i in l.strip().split("\n"))for l in open("g","r").read().split("\n\n")),reverse=True)[:3]))
