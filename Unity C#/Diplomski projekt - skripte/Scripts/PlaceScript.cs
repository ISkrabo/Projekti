using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlaceScript : MonoBehaviour
{
    Vector3 placePos;
    float placeRot;
    float length;
    // Start is called before the first frame update
    void Start()
    {
        length = this.transform.localScale.x / 2;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    
    void OnCollisionEnter(Collision col) {
        //provjeri da li je ispravni objekt postavljen
        if (col.gameObject.tag == "Pick") {

            //dohvati podatke od ciljnog mjesta (place)
            placePos = this.transform.position;
            placeRot = this.transform.rotation.eulerAngles.y;
            while (placeRot > 45f) {
                placeRot -= 90f;
            }

            //podaci stavljenog objekta (pick) i izracun preciznosti
            Vector3 pickPos = col.gameObject.transform.position;
            //usporedjujemo samo X i Z varijable, Y je vertikalna os
            //gledamo koliko je udaljeno od sredista s obzirom na duljinu objekta (polovicna jer gledamo apsolutnu vrijednost)
            float accuracyX = (length - Mathf.Abs(placePos.x - pickPos.x)) / length;
            float accuracyZ = (length - Mathf.Abs(placePos.z - pickPos.z)) / length;

            Debug.Log("Accuracy X " + accuracyX*100);
            Debug.Log("Accuracy Z " + accuracyZ*100);

            //ne moramo odredjivati koji vektor odredjuje rotaciju objekta, euler angle uvijek vraca relativnu rotaciju Y-osi naspram svijeta
            float pickRot = col.gameObject.transform.rotation.eulerAngles.y;
            while (pickRot > 45f) {
                pickRot -= 90f;
            }
            float accuracyRot = Mathf.Abs(placeRot - pickRot);
            Debug.Log("Rotation acc " + accuracyRot);
        }
    }
}
