function validAnagram(first, second) {

  // if the length of the 2 strings are not the same no need to continue
  if (first.length !== second.length) {
    return false;
  }
  const lookup = {};
  for (let i = 0; i < first.length; i++) {
    // this variable prevents me from calling i everytime
    let letter = first[i];
    // if letter exist,      increment,      otherwise set to 1
    lookup[letter] ? lookup[letter] += 1 : lookup[letter] = 1;
  }
  console.log(lookup)

  for (let i = 0; i < second.length; i++) {
    let letter = second[i];
    // cant find letter or letter is zero its not an Anagram
    if (!lookup[letter]) {
      return false;
    } else {
      lookup[letter] -= 1;
    }
  }
  return true;
}

console.log(validAnagram('anagrams', 'nagarams'))
// { a: 3, n: 1, g: 1, r: 1, m: 1, s: 1 }
// true

console.log(validAnagram('anams', 'samas'))
// { a: 2, n: 1, m: 1, s: 1 }
// false
