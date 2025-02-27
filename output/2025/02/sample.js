function getCoffeePrice() {
	const price = 300
	return price
}

function processOrder(quantity) {
  return new Promise((resolve) => {
    	const tax =  0.1
      const totalPrice = getCoffeePrice() * quantity
      resolve(totalPrice + totalPrice * tax)
  })
}

async function promiseFunc() {
  try {
    const quantity = 3
    console.log('promiseFunc before')
    totalPrice = await processOrder(quantity);
    console.log('promiseFunc after')
  } catch (e) {
    throw e
  }
}


let totalPrice = 0;
setTimeout(() => {
  console.log(`合計金額: ${totalPrice}円`)
}, 0)

promiseFunc()
console.log('計算中...')
