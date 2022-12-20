using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Test : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnCollisionStay (Collision other) {
        Debug.Log("sudar");
    }

    void OnTriggerStay (Collider other) {
        Debug.Log("trig");
    }

    void OnCollisionEnter(Collision other) {
        Debug.Log("sudar start");
    }
    void OnTriggerEnter (Collider other) {
        Debug.Log("trig start");
    }
}
