from dcv import core

handler = core.ODLP_Handler()
for result in handler.get_unchecked_results():
    print(result)
