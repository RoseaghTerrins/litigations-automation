import subprocess
import settings

subprocess.call(settings.FIRST_LOCATE_ACTIVITY_INCOMING_BATCH_FILE)

subprocess.call(settings.FIRST_LOCATE_AGMTS_INCOMING_BATCH_FILE)

subprocess.call(settings.FIRST_LOCATE_CLOSURE_INCOMING_BATCH_FILE)

subprocess.call(settings.FIRST_LOCATE_NFU_INCOMING_BATCH_FILE)

subprocess.call(settings.FIRST_LOCATE_QUERY_INCOMING_BATCH_FILE)

subprocess.call(settings.FIRST_LOCATE_TRANSACTION_INCOMING_BATCH_FILE)

subprocess.call(settings.YU_ADJUSTMENT_INCOMING_BATCH_FILE)

subprocess.call(settings.YU_NB_INCOMING_BATCH_FILE)

subprocess.call(settings.YU_QR_INCOMING_BATCH_FILE)

subprocess.call(settings.YU_CLOSURE_INCOMING_BATCH_FILE)

subprocess.call(settings.TO_JUST_AJJB_ACTIVITY)

subprocess.call(settings.TO_JUST_AJJB_CLOSURE)

subprocess.call(settings.TO_JUST_AJJB_NFU)

subprocess.call(settings.TO_JUST_AJJB_PAYMENT)

subprocess.call(settings.TO_JUST_AJJB_QUERIES)

subprocess.call(settings.FROM_CREDITSAFE_BATCHFILE)

subprocess.call(settings.FROM_Transunion_BATCHFILE)