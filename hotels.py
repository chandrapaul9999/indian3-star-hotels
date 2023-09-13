from playwright.sync_api import sync_playwright
import pandas as pd

def main():

    with sync_playwright() as p:

        checkin_date ='2023-09-13'
        checkout_date ='2023-09-17'



        
        page_url = f'https://www.booking.com/searchresults.en-gb.html?aid=7344211&label=metatripad-link-dmetain-hotel-2178483_xqdz-3326d8a63826265ee8cc047a7db92033_los-04_bw-000_tod-10_dom-in_curr-INR_gst-01_nrm-01_clkid-c33fa42c-d016-4dc9-8469-8ef5ec9afccf_aud-0000_mbl-L_pd-_sc-2_defdate-0_spo-0_clksrc-0_mcid-10&utm_medium=dmeta&no_rooms=1&show_room=217848301_97400747_2_1_0&utm_content=los-04_bw-000_dom-in_defdate-0_spo-0_clksrc-0&utm_campaign=in&utm_term=hotel-2178483&utm_source=metatripad&highlighted_hotels=2178483&checkin=2023-09-13&redirected=1&city=-2093298&hlrd=with_dates&group_adults=1&source=hotel&group_children=0&checkout=2023-09-17&keep_landing=1&sid=ac894d369b9d99d23c32bb3f12627d7b'

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto(page_url, timeout=60000)

        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'There are: {len(hotels)} hotels.')

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
            hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
            hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
            hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

            hotels_list.append(hotel_dict)

        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False)
        df.to_csv('hotels_list.csv', index=False)


        browser.close()


if __name__ == '__main__':
    main()
    
