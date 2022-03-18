from multiprocessing import Pool

from pypika import PostgreSQLQuery
from database import get_query_all
import electus
import epin


if __name__ == '__main__':
    print("test")
    #create_table()
    # electus.create_account(True)
    # update_username("59ab4d7916ab05d22db86258a2d83efd", "Test")
    # update_ep("181c0932e9735dcd15d80a77a662f80a", 43)
    # update_alchemy_time("59ab4d7916ab05d22db86258a2d83efd",(dt.now() - td(days=2)).strftime("%m/%d/%Y %H:%M:%S %p"))
    #pool = Pool()
    #pool.map(electus.create_account, range(20000))
    # electus.create_account()

    #electus.update_all_players_statics(5)


    #data_token = "UVcmKlKXClQA9627eyw9128gfWw0Q95iXYI0rOU1"
    #cookie = "__HFUID=97f5e60de9872e8ecbc15b219b13efc3;TOKEN=eyJpdiI6IloxM3EwdlNRRGtHYWFCVWM4azh0WEE9PSIsInZhbHVlIjoiRGxPaU5EYWVRc2g4M0NrL1NIWlZzMCtZU1RxZERKMUUyRHdkRFJ5R2pQZVFrcWZUcUY1Vld5amhDYncwYUlFMmtIKzdHdXBOb1ZzOHRPKy9uZnk0aHR3U3ZHM25mZ3BNQ0E1b3ltQVJKaWxLSmVKYXI4a25EejdRT1lzdTVkcFoiLCJtYWMiOiI0MDBiMGY5NGYzYWNhNDQyMDgxMDQyNWI4MDBjMWZhZGYyYjI5ZjQ1MGYxYTRiNmUzNjk3YzA3MWVlYWU5YzMwIiwidGFnIjoiIn0%3D;electus_session=eyJpdiI6IllhL284WThpMTZveWozYVpEMFFyaVE9PSIsInZhbHVlIjoiU1RhY1R0L2laQS8wcU1haCtJeSs1cEVqRXdIc1VGcmd3b0svdzdqd1E5S0tXRGp4VXp1Y2FKZmszMlRTYldVM1N0UTRWV3VrNXdmSm5IMDVlSWlQbHRWZVZCdm1jNXJROW1JMVRSM1QrQ0lLSjhFS2hOYTJIRFlTVWgwaU55MzAiLCJtYWMiOiI1ODg3ZTZlY2QwZjA3OGUyZmZhMDQyNTRkYzE0NzYzYmM0MGZjMDA4YzYyNTgwYWI2OWYwMjBkNTU4NmEyNWUxIiwidGFnIjoiIn0%3D;"
    #epin.use_all_epin_from_csv(cookie, data_token)



    # query = PostgreSQLQuery.from_('accounts').select('android_id')
    # query = str(query)
    # android_ids = get_query_all(query)
    # pool = Pool()
    # pool.map(epin.get_epins_from_account, android_ids)
