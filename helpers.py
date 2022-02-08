import sys


def reduce_text_len(text, max_len):
    if type(text) != str or type(max_len) != int:
        raise Exception("Parameters text & max_len must be str & int respectively.")

    reduced_text = ""
    text_len = len(text)
    if text_len <= max_len:
        return text
    else:
        count = 1
        current_word = ""
        for char in text:

            if char.isspace():
                reduced_text += current_word
                current_word = ""

                if count >= max_len:
                    reduced_text += "\n"
                    count = 0  # Reset counter
                else:
                    reduced_text += char
                    count += 1  # Increment

            else:
                current_word += char
                count += 1  # Increment

        reduced_text += current_word

        return reduced_text


if __name__ == "__main__":
    pass
