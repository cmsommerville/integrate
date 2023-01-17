export const STRING_MIN_LENGTH = (val: string, minLength: number) => {
    if (val.length < minLength) return false
    return true
}

export const STRING_MAX_LENGTH = (val: string, maxLength: number) => {
    if (val.length > maxLength) return false
    return true
}

export const ALPHANUMERIC_UNDERSCORE_HYPHEN = (val: string) => {
    return true
}