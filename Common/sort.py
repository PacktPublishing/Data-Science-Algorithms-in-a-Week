# ***Library implementing the sorting algorithms***


def quick_sort(seq, less_than):
    if len(seq) < 1:
        return seq
    else:
        pivot = seq[0]
        left = quick_sort(
            [x for x in seq[1:] if less_than(x, pivot)], less_than)
        right = quick_sort(
            [x for x in seq[1:] if not less_than(x, pivot)], less_than)
        return left + [pivot] + right
