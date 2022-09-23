import * as THREE from 'three'
import { Mesh, BufferGeometry, Material } from 'three'

const createSphere = (): THREE.Mesh => {
  const sphereGeometry = new THREE.SphereGeometry(16, 32, 16)
  const sphereMaterial = new THREE.MeshPhongMaterial({ color: 0x090fff })
  let sphere = new THREE.Mesh(sphereGeometry, sphereMaterial)
  return sphere
}

const createBox = (): THREE.Mesh => {
  const boxGeometry = new THREE.BoxGeometry(15, 15, 15)
  const boxMaterial = new THREE.MeshPhongMaterial({ color: 0xff9900 })
  let cube = new THREE.Mesh(boxGeometry, boxMaterial)
  return cube
}

const loadSubmergedObjects = (): THREE.Mesh[] => {
  // TODO Set up object loader
  // For now using a basic shapes is ok
  const submergedObjects: THREE.Mesh[] = []
  const amountOfObjects = 5 // Take this as param

  // Randomly creates the geometry + materials
  for (let i = 0; i < amountOfObjects; i++) {
    const randomNum = Math.floor(Math.random() * 2)
    if (randomNum == 1) {
      submergedObjects.push(createBox())
    } else {
      submergedObjects.push(createSphere())
    }
  }

  return submergedObjects
}

export const placeSubmergedObjects = () => {
  const submergedObjects = loadSubmergedObjects()

  // Sets up outer bounds
  const minXValue = -75
  const maxXValue = 75
  const minYValue = -1
  const maxYValue = 30
  const minZValue = -75
  const maxZValue = 75

  submergedObjects.forEach((submergedObject) => {
    submergedObject.position.y = 0.5

    // Randomizes position and rotation
    const submergedObjectRotation = Math.random() * Math.PI * 2
    submergedObject.position.x =
      Math.random() * (maxXValue - minXValue) + minXValue
    submergedObject.position.y =
      Math.random() * (maxYValue - minYValue) + minYValue
    submergedObject.position.z =
      Math.random() * (maxZValue - minZValue) + minZValue
    submergedObject.rotation.setFromVector3(
      new THREE.Vector3(0, submergedObjectRotation, 0),
    )
  })

  return submergedObjects
}
