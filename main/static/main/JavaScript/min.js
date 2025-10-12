deepEqual = function(fst, scnd) {

    if ("object" == (typeof scnd) && (typeof fst) == "object") {
        let count = 0
        if (scnd != null && fst != null) {
            for (let element of Object.keys(fst)) {
                for (let element_ of Object.keys(scnd)) {
                    count += deepEqual(fst[element], scnd[element_])
                }
            }
            if (count == Object.keys(fst).length && count == Object.keys(scnd).length)
                return true
        }

    } else {
        if (fst === scnd) {
            return true
        }
    }
    return false
}

loop = function(value, test, step, body) {
    if (test(value))
    {
        body(value);
        value = step(value);
        loop(value, next_value => next_value < 2, next_value => {return value + 1}, next_value => console.log(next_value));
    }
}

loop(-5, value => value < 2, value => {return value + 1}, value => console.log(value))

myEvery = function(array, func)
{
    if (!(array.some(value => !func(value))))
    {
        return true;
    } else
    {
        return false;
    }
}

myEvery = function(array, func)
{
    let yes = 0;
    for (let value of array)
    {
        if (func(value))
        {
            yes += 1;
        }
    }
    if (yes == array.length)
    {
        return true;
    } else
    {
        return false;
    }
}

array = [1, 2, 3, 4, 5, 6]
console.log(myEvery(array, (value) => value < 10))

