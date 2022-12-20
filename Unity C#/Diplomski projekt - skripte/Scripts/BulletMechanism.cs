using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BulletMechanism : MonoBehaviour
{

    float velocity;
    Vector3 direction;
    float life = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        transform.position = Vector3.MoveTowards(transform.position, transform.position + transform.forward, velocity * Time.deltaTime);
        life += Time.deltaTime;

        if (life > 1.0f) {
            Destroy(this.gameObject);
        }


    }
    
    private void OnTriggerEnter(Collider other) {
        if (other.tag != "Player") {
            Debug.Log(other);
            Debug.Log(other.name);
            Destroy(this.gameObject);
        }
    }

    public void SetValues(float val, Vector3 dir) {
        velocity=val;
        transform.rotation = Quaternion.LookRotation(dir);
    }
}
